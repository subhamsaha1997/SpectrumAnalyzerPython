from PyQt5.QtCore import QObject, pyqtSignal as Signal
from Radio import USRP
from Queue import Full

class RadioStreamer(QObject):
	""" This wraps the USRP object with QObject class to support signals and slots"""
	radioSetup = Signal(str)
	radioStarted = Signal(str)
	radioStopped = Signal(str)
	radioHold = Signal()

	def __init__(self,parent = None):
		super(RadioStreamer,self).__init__(parent)
		self.radio = radio = USRP()
		self.isLive = False
	# setup the usrp device
	def setup(self,args,status):
		
		obtainedSettings = self.radio.setupDevice(args['centerFrequency'],args['bandwidth'],args['gain'])
		self.radioSetup.emit("Center frequency: {} Hz Bandwidth: {}Hz Gain: {}dB ".format(
				obtainedSettings['centerFrequency'],obtainedSettings['bandwidth'],obtainedSettings['gain']))
		self.isLive = status
	# stream samples to queue for plotting
	def stream(self,queue,fftsize=4096,window='none',update_interval=0.08):
		self.radioStarted.emit('ON')
		while not self.isLive.is_set():
			try:
				queue.put(self.radio.getFrequencyResponse(fftsize,window,update_interval),timeout=5)
			except Full:
				time.sleep(1)
		self.radioStopped.emit('OFF')
	# record samples to specified file
	def record(self,filename,num_samples):
		self.radioStarted.emit('ON')
		self.radio.saveToFile(filename,num_samples)
		self.radioStopped.emit('OFF')



