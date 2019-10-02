from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import *
from Widgets import *
from Parameter import usrp_parameters
import copy

class MapSettings(QWidget):
	""" Groups all the map settings and defines signals and slots"""
	recordRequested = Signal(dict)
	locationRequested = Signal()


	def __init__(self,parent = None):
		super(MapSettings,self).__init__(parent)
		self.usrp_parameters = copy.deepcopy(usrp_parameters)
		self.centerFrequency = centerFrequency = CenterFrequency()
		self.bandwidth = bandwidth = Bandwidth()
		self.gain = gain = Gain()
		self.recordTime = recordTime = RecordTime()
		self.display = display = CurrentPositionDisplay(('Latitude','Longitude'))

		self.controls = controls = MapControls()

		layout = QVBoxLayout()
		layout.addWidget(centerFrequency)
		layout.addWidget(bandwidth)
		layout.addWidget(gain)
		layout.addWidget(recordTime)
		layout.addWidget(display)
		layout.addWidget(controls)
		layout.addStretch(1)
		self.setLayout(layout)

		centerFrequency.valueChanged.connect(self.updateCenterFrequency)
		bandwidth.valueChanged.connect(self.updateBandwidth)
		gain.valueChanged.connect(self.updateGain)
		recordTime.valueChanged.connect(self.updateRecordTime)
		controls.locate.connect(lambda: self.locationRequested.emit())
		controls.record.connect(lambda: self.recordRequested.emit(self.usrp_parameters))

	def locationNotFound(self):
		self.controls.lockRecord()
	def locationFound(self):
		self.controls.unlockRecord()

	def updateCenterFrequency(self,val):
		self.usrp_parameters['centerFrequency'] = val

	def updateBandwidth(self,val):
		self.usrp_parameters['bandwidth'] = val

	def updateGain(self,val):
		self.usrp_parameters['gain'] = val

	def updateRecordTime(self,val):
		self.usrp_parameters['recordTime'] = val


if __name__ == '__main__':
	app = QApplication([])
	m = MapSettings()
	m.show()
	app.exec_()
	

	
