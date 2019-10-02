from PyQt5.QtCore import Qt, pyqtSignal as Signal
from PyQt5.QtWidgets import *
from GridSettings import GridSettings
from Canvas3D import Canvas3D

class GridWidget(QWidget):
	""" sets up the grid widget and defines necessary signals and slots"""
	startRecord = Signal(dict,str)


	def __init__(self,parent = None):
		super(GridWidget,self).__init__(parent)
		self.canvas = Canvas3D()
		self.gridSettings = gridSettings  = GridSettings()

		splitter = QSplitter(Qt.Horizontal)
		splitter.addWidget(self.canvas)
		splitter.addWidget(gridSettings)
		splitter.setStretchFactor(0,3)
		splitter.setStretchFactor(1,1)

		layout = QHBoxLayout()
		layout.addWidget(splitter)

		self.setLayout(layout)
		gridSettings.recordRequested.connect(self.record)
		gridSettings.initgrid.connect(self.canvas.init)

	def getPosition(self):
		return [self.gridSettings.position['x'],self.gridSettings.position['y']]


	def record(self,params):
		params['position'] = self.getPosition()
		params['step'] = [self.gridSettings.xstep,self.gridSettings.ystep]
		self.startRecord.emit(params,'GRID')



if __name__ == '__main__':
	app = QApplication([])
	m = GridWidget()
	m.show()
	app.exec_()
