from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import *
from Widgets import *
from Parameter import usrp_parameters
import copy

class PlotSettings(QWidget):
	""" Groups all the plot control widgets and defines necessary signals and slots"""
	recordRequested = Signal(dict)
	plotRequested = Signal(dict)
	

	def __init__(self,parent = None):
		super(PlotSettings,self).__init__(parent)
		self.usrp_parameters = copy.deepcopy(usrp_parameters)
		self.centerFrequency = centerFrequency = CenterFrequency()
		self.bandwidth = bandwidth = Bandwidth()
		self.gain = gain = Gain()
		self.fftproperty = fftproperty = FFTProperty()
		self.recordTime = recordTime = RecordTime()

		self.controls = controls = PlotandRecordControl()

		layout = QVBoxLayout()
		layout.addWidget(centerFrequency)
		layout.addWidget(bandwidth)
		layout.addWidget(gain)
		layout.addWidget(fftproperty)
		layout.addWidget(recordTime)
		
		layout.addWidget(controls)
		layout.addStretch(1)
		self.setLayout(layout)

		
		centerFrequency.valueChanged.connect(self.updateCenterFrequency)
		bandwidth.valueChanged.connect(self.updateBandwidth)
		gain.valueChanged.connect(self.updateGain)
		recordTime.valueChanged.connect(self.updateRecordTime)
		fftproperty.sizeChanged.connect(self.updateFFTSize)
		fftproperty.windowChanged.connect(self.updateFFTWindow)
		controls.startRecord.connect(lambda: self.recordRequested.emit(self.usrp_parameters))
		controls.startPlot.connect(lambda: self.plotRequested.emit(self.usrp_parameters))
	

	def updateCenterFrequency(self,val):
		self.usrp_parameters['centerFrequency'] = val
		print(self.usrp_parameters)

	def updateBandwidth(self,val):
		self.usrp_parameters['bandwidth'] = val

	def updateGain(self,val):
		self.usrp_parameters['gain'] = val

	def updateRecordTime(self,val):
		self.usrp_parameters['recordTime'] = val
	def updateFFTSize(self,val):
		self.usrp_parameters['fftsize'] = val
	def updateFFTWindow(self,val):
		self.usrp_parameters['window'] = val


if __name__ == '__main__':
	app = QApplication([])
	m = PlotSettings()
	m.show()
	app.exec_()
	

	
