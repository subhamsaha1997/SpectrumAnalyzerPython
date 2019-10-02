from PyQt5.QtCore import Qt, pyqtSignal as Signal
from PyQt5.QtWidgets import *
from PlotSettings import PlotSettings
from Canvas2D import Canvas2D

class ViewWidget(QWidget):
	""" Sets up the view tab """
	startRecord = Signal(dict,str)
	startPlot = Signal(dict)


	def __init__(self,parent = None):
		super(ViewWidget,self).__init__(parent)
		self.canvas = Canvas2D()
		self.plotSettings = plotSettings  = PlotSettings()

		splitter = QSplitter(Qt.Horizontal)
		splitter.addWidget(self.canvas)
		splitter.addWidget(plotSettings)
		splitter.setStretchFactor(0,3)
		splitter.setStretchFactor(1,1)

		layout = QHBoxLayout()
		layout.addWidget(splitter)

		self.setLayout(layout)
		plotSettings.recordRequested.connect(self.record)
		plotSettings.plotRequested.connect(self.plot)


	def record(self,params):
		self.startRecord.emit(params,'VIEW')

	def plot(self,params):
		self.startPlot.emit(params)




if __name__ == '__main__':
	app = QApplication([])
	m = ViewWidget()
	m.show()
	app.exec_()
