import uhd.libpyuhd as lib
import numpy as np
import time

class USRP(lib.usrp.multi_usrp):
	""" Defines the USRP object to be interfaced in the application"""

	def __init__(self):
		deviceargs = "type=b200,recv_frame_size=12000"
		self.params = {}

		trials = 5
		while trials > 0:
			try:
				super(USRP,self).__init__(deviceargs)
				break
			except RuntimeError,e:
				time.sleep(0.1)
				trials = trials - 1

	def setCenterFreq(self,f=2.45e9,chan=0):
		super(USRP,self).set_rx_freq(lib.types.tune_request(f),chan)
		return super(USRP,self).get_rx_freq()

	def setSamplingFreq(self,f=4e6,chan=0):
		try:
			super(USRP,self).set_rx_rate(f,chan)
			self.setBandwidth(f)
		except RuntimeError,e:
			super(USRP,self).set_rx_rate(1e6,chan)
			self.setBandwidth(1e6)
		return super(USRP,self).get_rx_rate()

	def setGain(self,g=30,chan=0):
		super(USRP,self).set_rx_gain(g)
		return super(USRP,self).get_rx_gain()

	def setBandwidth(self,bw):
		super(USRP,self).set_rx_bandwidth(bw)

	def setMasterClockRate(self,rate):
		super(USRP,self).set_master_clock_rate(rate)

	def setAgc(self,channel=0):
		self.set_rx_agc(True,channel)

	def unsetAgc(self,channel=0):
		self.set_rx_agc(False,channel)

	def setupDevice(self,centerFreq=2.45e9,samplingFreq=4e6,gain=30,agc=False):
		if agc:
			self.setAgc()
		self.setMasterClockRate(8*samplingFreq)
		args = {"centerFrequency":self.setCenterFreq(centerFreq),"bandwidth":self.setSamplingFreq(samplingFreq),"gain":self.setGain(gain)}
		self.params = args
		
		self.average = None
		self.averageCount = 0;
		return args


	# to get the frequency response after capturing the data
	def getFrequencyResponse(self,fftsize = 4096,window = 'none',update_interval=0.1,timeout=1):

		stream_args = lib.usrp.stream_args("fc32","sc16")
		stream_args.channels = (0,)
		metadata = lib.types.rx_metadata()
		streamer = super(USRP,self).get_rx_stream(stream_args)
		buffSize = streamer.get_max_num_samps()
		result = np.empty(fftsize,dtype = np.complex64)
		recv_buffer = np.zeros((1,buffSize),dtype=np.complex64)
		samps = 0

		recv_samps = 0
		time_elapsed = 0
		stream_cmd = lib.types.stream_cmd(lib.types.stream_mode.num_done)
		stream_cmd.num_samps = fftsize
		stream_cmd.stream_now = True
		streamer.issue_stream_cmd(stream_cmd)
		tstart = time.time()
		

		while recv_samps < fftsize:
			try:
				samps = streamer.recv(recv_buffer,metadata)

				if metadata.error_code != lib.types.rx_metadata_error_code.none:
					raise OverflowException
				if samps:
					real_samps = min(fftsize - recv_samps,samps)
					result[recv_samps:recv_samps+real_samps] = recv_buffer[0,0:real_samps]
					recv_samps += real_samps
			except OverflowException:
				pass
		data = self.frequencyResponse(result,window)
		time_elapsed = time.time()-tstart
		if time_elapsed < update_interval:
			time.sleep(update_interval-time_elapsed)

		return data

	# to calculate frequency response
	def frequencyResponse(self,samples,window):
		l = samples.size
		if window != 'none':
			samples = smooth(samples,window)
		data = np.abs(np.fft.fftshift(np.fft.fft(samples)))
		return data

	# to save to a file
	def saveToFile(self,filename,numSamps=2**10):
		with open(filename,'wb') as fid:

			stream_args = lib.usrp.stream_args("fc32","sc16")
			stream_args.channels = (0,)
			metadata = lib.types.rx_metadata()
			streamer = super(USRP,self).get_rx_stream(stream_args)
			buffSize = streamer.get_max_num_samps()
			recv_buffer = np.zeros((1,buffSize),dtype=np.complex64)
			samps = np.array([],dtype=np.complex64)

			recv_samps = 0
			stream_cmd = lib.types.stream_cmd(lib.types.stream_mode.start_cont)
			stream_cmd.stream_now = True
			streamer.issue_stream_cmd(stream_cmd)
			overflow = False

			while recv_samps < numSamps:
				try:
					samps = streamer.recv(recv_buffer,metadata)

					if metadata.error_code == lib.types.rx_metadata_error_code.overflow:
						raise OverflowException
					elif samps:
						real_samps = min(numSamps - recv_samps,samps)
						fid.write(recv_buffer[:,0:real_samps])
						recv_samps += real_samps
				except OverflowException:
					overflow = True
					break

			fid.close()
			stream_cmd = lib.types.stream_cmd(lib.types.stream_mode.stop_cont)
			streamer.issue_stream_cmd(stream_cmd)

			while samps:
				samps = streamer.recv(recv_buffer,metadata)

			if overflow:
				raise OverflowException




class OverflowException(Exception):
	""" Overflow Occurred """
	pass

# to apply smoothing
def smooth(samples,window):
	size = len(samples)
	w = getattr(np,window)(size)
	return w*samples


