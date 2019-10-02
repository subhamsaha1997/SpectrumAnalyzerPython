from PyQt5.QtCore import Qt, pyqtSignal as Signal
from PyQt5.QtWidgets import *
from Map import Mapview
from MapSettings import MapSettings
from GPS import GPSObject

class GPSWidget(QWidget):
	""" Provides methods to connect to the GPS module"""
	noGpsdevice = Signal()
	noPositionLock = Signal()
	startRecord = Signal(dict,str)


	def __init__(self,parent = None):
		super(GPSWidget,self).__init__(parent)
		self.map = Mapview()
		self.mapSettings = mapSettings  = MapSettings()
		self.currentPosition = (None,None)

		splitter = QSplitter(Qt.Horizontal)
		splitter.addWidget(self.map)
		splitter.addWidget(mapSettings)
		splitter.setStretchFactor(0,3)
		splitter.setStretchFactor(1,1)

		layout = QHBoxLayout()
		layout.addWidget(splitter)

		self.setLayout(layout)
		mapSettings.locationRequested.connect(self.getLocation)
		mapSettings.recordRequested.connect(self.record)

	def getLocation(self):
		try:
			gps = GPSObject()
			position = gps.Position()
			if (position[0] is None):
				print ('Location Not Found!')
				self.noPositionLock.emit()
				self.mapSettings.locationNotFound()
			else:
				self.mapSettings.locationFound()
				self.currentPosition = position
				self.map.addMarker(position)
				self.mapSettings.display.updatePosition(position)
				return position
		except Exception,e:
			self.mapSettings.locationNotFound()
			self.noGpsdevice.emit()


	def record(self,params):
		try:
			params['position'] = self.currentPosition
		except Exception,e:
			print(e)
			return
		self.startRecord.emit(params,'MAP')



if __name__ == '__main__':
	app = QApplication([])
	m = GPSWidget()
	m.show()
	app.exec_()
