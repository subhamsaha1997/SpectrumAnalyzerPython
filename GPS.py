import serial
import time
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal as Signal

class GPSObject(QObject):

	def __init__(self):
		super(GPSObject,self).__init__()
		port = '/dev/ttyUSB0'
		self.ser = None
		try:
			self.ser = serial.Serial(port,baudrate=4800)
			self.ser.close()
		except serial.SerialException, e:
			raise Exception("No device found.")

	def getPosition(self,data,sentence="$GPRMC"):
		if data[0:6] == sentence:
			splittedData = data.split(',')
			if splittedData[2] == 'A':
				latString = splittedData[3]
				north = (splittedData[4]=='N')
				lngString = splittedData[5]
				east = (splittedData[6]=='E')
				temp = float(latString)
				lat = (temp -temp%100)/100 + (temp%100)/60
				if not north:
					lat = (-1)*lat
				temp = float(lngString)
				lng = (temp -temp%100)/100 + (temp%100)/60
				if not east:
					lng = (-1)*lng
				return (lat,lng)
		return None

	def observe(self,observations=5,timeout=10):
		if(self.ser):
			self.ser.open()
			start = time.time()
			result = []
			count = 0;
			while True:
				line = self.ser.readline()
				r = self.getPosition(line)
				if(r):
					result.append(r)
					count += 1
				if (count >= observations):
					break
				elif(time.time()-start > timeout):
					break
			self.ser.close()
			return (count,result)
		else:
			return None
	def Position(self):
		(count,result) = self.observe()
		if(count>0):
			mat = np.transpose(np.asarray(result))
			lat = mat[0].mean()
			lng = mat[1].mean()
			print(lat,lng)
			return [lat,lng]
		else:
			return [None,None]



if __name__ == '__main__':
	gps = GPSObject()
	print(gps.Position())


		


