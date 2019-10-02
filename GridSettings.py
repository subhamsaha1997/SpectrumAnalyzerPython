from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import *
from Widgets import *
from Parameter import usrp_parameters
import copy

class GridSettings(QWidget):
	""" groups the grid control widgets """
	recordRequested = Signal(dict)
	initgrid = Signal(float,float)
	

	def __init__(self,parent = None):
		super(GridSettings,self).__init__(parent)
		self.usrp_parameters = copy.deepcopy(usrp_parameters)
		self.centerFrequency = centerFrequency = CenterFrequency()
		self.bandwidth = bandwidth = Bandwidth()
		self.gain = gain = Gain()
		self.recordTime = recordTime = RecordTime()
		self.size = size = GridSize()
		self.stepSize = stepSize = StepSize()
		self.display = display = CurrentPositionDisplay(('X-Position (meters)','Y-Position (meters)'))

		self.controls = controls = GridControls()

		layout = QVBoxLayout()
		layout.addWidget(centerFrequency)
		layout.addWidget(bandwidth)
		layout.addWidget(gain)
		layout.addWidget(recordTime)
		layout.addWidget(size)
		layout.addWidget(stepSize)
		layout.addWidget(display)
		layout.addWidget(controls)
		layout.addStretch(1)
		self.setLayout(layout)

		self.position = {
		'x':0,
		'y':0
		}
		self.xstep = 0.1
		self.ystep = 0.1

		centerFrequency.valueChanged.connect(self.updateCenterFrequency)
		bandwidth.valueChanged.connect(self.updateBandwidth)
		gain.valueChanged.connect(self.updateGain)
		recordTime.valueChanged.connect(self.updateRecordTime)
		controls.record.connect(self.startRecord)
		size.initPressed.connect(self.initGrid)
		stepSize.xstepUpdated.connect(self.updatexStep)
		stepSize.ystepUpdated.connect(self.updateyStep)
		controls.leftPressed.connect(self.decrXPosition)
		controls.rightPressed.connect(self.incrXPosition)
		controls.upPressed.connect(self.incrYPosition)
		controls.downPressed.connect(self.decrYPosition)

	def updatexStep(self,val):
		self.xstep = val
	def updateyStep(self,val):
		self.ystep = val
	def initGrid(self,size):
		self.initgrid.emit(size[0],size[1])

	def incrXPosition(self):
		self.position['x'] += self.xstep
		self.display.updatePosition((self.position['x'],self.position['y']))
	def incrYPosition(self):
		self.position['y'] += self.ystep
		self.display.updatePosition((self.position['x'],self.position['y']))
	def decrXPosition(self):
		self.position['x'] -= self.xstep
		self.display.updatePosition((self.position['x'],self.position['y']))
	def decrYPosition(self):
		self.position['y'] -= self.ystep
		self.display.updatePosition((self.position['x'],self.position['y']))


	def updateCenterFrequency(self,val):
		self.usrp_parameters['centerFrequency'] = val

	def updateBandwidth(self,val):
		self.usrp_parameters['bandwidth'] = val

	def updateGain(self,val):
		self.usrp_parameters['gain'] = val

	def updateRecordTime(self,val):
		self.usrp_parameters['recordTime'] = val

	def startRecord(self):
		print(self.usrp_parameters)
		self.recordRequested.emit(self.usrp_parameters)


if __name__ == '__main__':
	app = QApplication([])
	m = GridSettings()
	m.show()
	app.exec_()
	

	
