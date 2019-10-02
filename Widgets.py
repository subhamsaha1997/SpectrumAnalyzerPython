from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import *

from Parameter import *

class Gain(QWidget):
	""" The gain control widget"""
	valueChanged = Signal(float)

	def __init__(self, parent = None):
		super(Gain,self).__init__(parent)

		self.slider = slider = QSlider(Qt.Horizontal)
		slider.setRange(0,maxGain)
		slider.setSingleStep(1)
		slider.setValue(30)

		self.spinbox = spinbox = QDoubleSpinBox()
		spinbox.setRange(0,maxGain)
		spinbox.setSingleStep(0.1)
		spinbox.setValue(30)

		label = QLabel('&Gain')
		label.setBuddy(spinbox)

		layout1 = QHBoxLayout()
		
		layout1.addWidget(slider)
		layout1.addWidget(spinbox)

		layout = QVBoxLayout()
		layout.addWidget(label)
		layout.addLayout(layout1)

		self.setLayout(layout)
		spinbox.valueChanged.connect(self.spinboxValueChanged)
		slider.valueChanged.connect(self.sliderValueChanged)

	def spinboxValueChanged(self,val):
		self.slider.setValue(val)
		self.valueChanged.emit(val)

	def sliderValueChanged(self,val):
		self.spinbox.setValue(val)

class CenterFrequency(QWidget):
	""" The center frequency control widget"""
	valueChanged = Signal(float)
	

	def __init__(self,parent = None):
		super(CenterFrequency,self).__init__(parent)

		self.centerFrequency = centerFrequency = QDoubleSpinBox()
		centerFrequency.setRange(minCenterFrequency,maxCenterFrequency)
		centerFrequency.setSingleStep(1e5)
		centerFrequency.setValue(2.45e9)
		label = QLabel('Center &Frequency (Hz)')
		label.setBuddy(centerFrequency)

		layout = QVBoxLayout()
		layout.addWidget(label)
		layout.addWidget(centerFrequency)
		self.setLayout(layout)

		centerFrequency.valueChanged.connect(self.centerFrequencyChanged)

	def centerFrequencyChanged(self,val):
		self.valueChanged.emit(val)

class Bandwidth(QWidget):
	""" The bandwidth control widget"""
	valueChanged = Signal(float)
	def __init__(self,parent = None):
		super(Bandwidth,self).__init__(parent)
		

		self.bandwidth = bandwidth = QDoubleSpinBox()
		bandwidth.setRange(minBandwidth,maxBandwidth)
		bandwidth.setSingleStep(10e3)
		bandwidth.setValue(4e6)
		label = QLabel('&Bandwidth (Hz)')
		label.setBuddy(bandwidth)

		layout = QVBoxLayout()
		layout.addWidget(label)
		layout.addWidget(bandwidth)
		self.setLayout(layout)

		bandwidth.valueChanged.connect(self.bandwidthChanged)

	def  bandwidthChanged(self,val):
		self.valueChanged.emit(val)



class RecordTime(QWidget):
	""" The record time control widget"""
	valueChanged = Signal(float)
	
	def __init__(self,parent=None):
		super(RecordTime,self).__init__(parent)

		self.time = time = QDoubleSpinBox()
		time.setDecimals(2)
		time.setSuffix(' seconds')
		time.setRange(0,maxRecordTime)
		time.setSingleStep(0.01)
		time.setValue(1)

		label = QLabel('&Record Time')
		label.setBuddy(time)
		layout = QVBoxLayout()
		layout.addWidget(label)
		layout.addWidget(time)

		self.setLayout(layout)

		time.valueChanged.connect(self.timeChanged)

	def timeChanged(self,val):
		self.valueChanged.emit(val)

class FFTProperty(QWidget):
	""" The FFT property control widget"""
	sizeChanged = Signal(int)
	windowChanged = Signal(str)

	def __init__(self,parent = None):
		super(FFTProperty,self).__init__(parent)
		self.fftsize = fftsize = QComboBox()
		fftsize.addItems(['512','1024','2048','4096','8192'])
		fftsize.setCurrentIndex(3)
		self.fftwindow = fftwindow = QComboBox()
		fftwindow.addItems(['none','hamming','hanning','blackman'])

		label1 = QLabel('FFT &Size')
		label1.setBuddy(fftsize)

		label2 = QLabel('FFT Window')
		label2.setBuddy(fftwindow)

		layout = QGridLayout()
		layout.addWidget(label1,0,0,1,1)
		layout.addWidget(fftsize,0,1,1,1)
		layout.addWidget(label2,1,0,1,1)
		layout.addWidget(fftwindow,1,1,1,1)

		self.setLayout(layout)

		fftsize.currentIndexChanged.connect(self.fftsizeChanged)
		fftwindow.currentIndexChanged.connect(self.fftwindowChanged)

	def fftsizeChanged(self):
		i = int(self.fftsize.currentText())
		self.sizeChanged.emit(int(i))

	def fftwindowChanged(self):
		w = self.fftwindow.currentText()
		self.windowChanged.emit(w)

class PlotandRecordControl(QWidget):
	""" Provides control for plot and record view"""
	startPlot = Signal()
	startRecord = Signal()

	def __init__(self,parent = None):
		super(PlotandRecordControl,self).__init__(parent)
		layout = QHBoxLayout()
		self.plot = plot = QPushButton('&Update/Start')
		self.record = record = QPushButton('&Record')

		layout.addWidget(plot)
		layout.addWidget(record)
		self.setLayout(layout)

		plot.clicked.connect(self.startPlotting)
		record.clicked.connect(self.startRecording)

	def startPlotting(self):
		self.startPlot.emit()
	def startRecording(self):
		self.startRecord.emit()

class GridSize(QWidget):
	""" to modify grid size"""
	initPressed = Signal(tuple)

	def __init__(self,parent = None):
		super(GridSize,self).__init__(parent)
		label1 = QLabel("X-Size (meter)")
		self.xsize = xsize = QDoubleSpinBox()
		label1.setBuddy(xsize)

		label2 = QLabel("Y-Size (meter)")
		self.ysize = ysize = QDoubleSpinBox()
		label2.setBuddy(ysize)

		initbutton = QPushButton('&Update')

		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		hbox1.addWidget(label1)
		hbox1.addWidget(xsize)
		hbox2.addWidget(label2)
		hbox2.addWidget(ysize)

		layout = QVBoxLayout()
		layout.addLayout(hbox1)
		layout.addLayout(hbox2)
		layout.addWidget(initbutton)
		self.setLayout(layout)

		self.size = size = [2,2]

		xsize.valueChanged.connect(self.xupdate)
		ysize.valueChanged.connect(self.yupdate)
		initbutton.clicked.connect(lambda: self.initPressed.emit((size[0],size[1])))

	def xupdate(self,val):
		self.size[0] = val
	def yupdate(self,val):
		self.size[1] = val

class StepSize(QWidget):
	""" To modify step size in grid view"""
	xstepUpdated = Signal(float)
	ystepUpdated = Signal(float)

	def __init__(self,parent = None):
		super(StepSize,self).__init__(parent)
		label1 = QLabel('X-Step Size (meter)')
		self.xstep = xstep = QDoubleSpinBox()
		label1.setBuddy(xstep)
		xstep.setRange(0,maxStepSize)
		xstep.setSingleStep(singleStep)
		xstep.setValue(0.1)

		label2 = QLabel('Y-Step Size (meter)')
		self.ystep = ystep = QDoubleSpinBox()
		label2.setBuddy(ystep)
		ystep.setRange(0,maxStepSize)
		ystep.setSingleStep(singleStep)
		ystep.setValue(0.1)

		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		hbox1.addWidget(label1)
		hbox1.addWidget(xstep)
		hbox2.addWidget(label2)
		hbox2.addWidget(ystep)

		layout = QVBoxLayout()
		layout.addLayout(hbox1)
		layout.addLayout(hbox2)
		self.setLayout(layout)


		xstep.valueChanged.connect(lambda val: self.xstepUpdated.emit(val))
		ystep.valueChanged.connect(lambda val: self.ystepUpdated.emit(val))

class CurrentPositionDisplay(QWidget):
	""" Position display for grid and GPS view"""

	def __init__(self,names,parent = None):
		super(CurrentPositionDisplay,self).__init__(parent)
		label1 = QLabel(names[0])
		self.pos1 = pos1 = QLabel('0')
		label2 = QLabel(names[1])
		self.pos2 = pos2 = QLabel('0')

		layout = QGridLayout()
		layout.addWidget(label1,0,0,1,1)
		layout.addWidget(pos1,0,1,1,1)
		layout.addWidget(label2,1,0,1,1)
		layout.addWidget(pos2,1,1,1,1)
		self.setLayout(layout)

	def updatePosition(self,position):
		self.pos1.setText(str(position[0]))
		self.pos2.setText(str(position[1]))


class GridControls(QWidget):
	""" Controls for the grid view"""
	leftPressed = Signal()
	rightPressed = Signal()
	upPressed = Signal()
	downPressed = Signal()
	record = Signal()

	def __init__(self,parent = None):
		super(GridControls,self).__init__(parent)
		gridlayout = QGridLayout()
		self.l = l =QPushButton('X-')
		self.r = r = QPushButton('X+')
		self.u = u = QPushButton('Y+')
		self.d = d = QPushButton('Y-')

		gridlayout.addWidget(l,1,0,1,1)
		gridlayout.addWidget(r,1,2,1,1)
		gridlayout.addWidget(u,0,1,1,1)
		gridlayout.addWidget(d,2,1,1,1)

		self.recordButton = recordButton = QPushButton('&Record')

		vbox = QVBoxLayout()
		vbox.addLayout(gridlayout)
		vbox.addWidget(recordButton)

		self.setLayout(vbox)

		l.clicked.connect(self.leftKeyPressed)
		r.clicked.connect(self.rightKeyPressed)
		u.clicked.connect(self.upKeyPressed)
		d.clicked.connect(self.downKeyPressed)
		recordButton.clicked.connect(self.startRecording)

	def startRecording(self):
		self.record.emit()
	def leftKeyPressed(self):
		self.leftPressed.emit()
	def rightKeyPressed(self):
		self.rightPressed.emit()
	def upKeyPressed(self):
		self.upPressed.emit()
	def downKeyPressed(self):
		self.downPressed.emit()

class MapControls(QWidget):
	""" Controls for the map view"""
	locate = Signal()
	record = Signal()

	def __init__(self,parent = None):
		super(MapControls,self).__init__(parent)
		self.locateButton = locateButton = QPushButton('&Locate')
		self.recordButton = recordButton = QPushButton('&Record')
		layout = QHBoxLayout()
		layout.addWidget(locateButton)
		layout.addWidget(recordButton)
		recordButton.setEnabled(False)
		self.setLayout(layout)

		locateButton.clicked.connect(lambda: self.locate.emit())
		recordButton.clicked.connect(lambda: self.record.emit())

	def lockRecord(self):
		self.recordButton.setEnabled(False)

	def unlockRecord(self):
		self.recordButton.setEnabled(True)




"""
class BasicProperties(QWidget):


	def __init__(self,parent = None):
		super(BasicProperties,self).__init__(parent)
		self.centerFrequency = centerFrequency = CenterFrequency()

		self.bandwidth = bandwidth = Bandwidth()

		self.gain = gain = Gain()

		self.recordtime = recordtime = RecordTime()

		self.fftprops = fftprops = FFTProperty()

		grpbox = QGroupBox('Settings')
		grp1 = QVBoxLayout()

		grp1.addWidget(centerFrequency)
		grp1.addWidget(bandwidth)
		grp1.addWidget(gain)
		grp1.addWidget(recordtime)
		grp1.addWidget(fftprops)
		grpbox.setLayout(grp1)
		layout = QVBoxLayout()
		layout.addWidget(grpbox)
		self.setLayout(layout)

		centerFrequency.valueChanged.connect(self.printValue)
		bandwidth.valueChanged.connect(self.printValue)
		gain.valueChanged.connect(self.printValue)
		recordtime.valueChanged.connect(self.printValue)
		fftprops.sizeChanged.connect(self.printValue)
		fftprops.windowChanged.connect(self.printValue)

	def printValue(self,val):
		print "Value changed to: {:f}".format(val)

class MyMainWindow(QMainWindow):

	def __init__(self,parent = None):
		super(MyMainWindow,self).__init__(parent)
		self.widget = widget = BasicProperties()
		self.setCentralWidget(widget)
		

if __name__ == '__main__':
	app = QApplication([])
	m = MyMainWindow()
	m.show()
	app.exec_()
"""



