from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from GPSWidget import GPSWidget
from ViewWidget import ViewWidget
from GridWidget import GridWidget
from multiprocessing import Event, Queue
import subprocess
from RadioWrapper import *
import numpy as np

class Worker(QRunnable):
	""" to handle multiple threads in Qt"""
	def __init__(self,fn,*args,**kwargs):
		super(Worker,self).__init__()
		self.fn = fn
		self.args = args
		self.kwargs = kwargs

	def run(self):
		self.fn(*self.args,**self.kwargs)

class MainWindow(QMainWindow):
	""" sets up the main window"""

	def __init__(self,parent = None):
		super(MainWindow,self).__init__(parent)
		self.setWindowTitle("Spectrum Sense")

		self.view = view = ViewWidget()
		self.grid = grid = GridWidget()
		self.gps = gps = GPSWidget()
		self.textUpdate = textUpdate = QTextBrowser()

		tabwidget = QTabWidget()
		tabwidget.addTab(view,'View')
		tabwidget.addTab(grid,'Grid')
		tabwidget.addTab(gps,'GPS')

		splitter = QSplitter(Qt.Vertical)
		splitter.addWidget(tabwidget)
		splitter.addWidget(textUpdate)
		splitter.setStretchFactor(0,3)
		splitter.setStretchFactor(1,1)

		self.setCentralWidget(splitter)

		view.startRecord.connect(self.record)
		grid.startRecord.connect(self.record)
		gps.startRecord.connect(self.record)
		gps.noGpsdevice.connect(lambda: self.textUpdate.append('[GPS] No device found.'))
		gps.noPositionLock.connect(lambda: self.textUpdate.append('[GPS] Position lock not obtained.'))

		view.startPlot.connect(self.plot)

		self.radio = radio = RadioStreamer()

		self.plotEvent = Event()
		self.threadpool = QThreadPool()
		self.dataqueue = Queue()
		self.threadpool.setMaxThreadCount(2)

	def plot(self,params):
		""" method for plotting"""
		if not self.plotEvent.is_set():
			self.plotEvent.set()
		self.threadpool.waitForDone()
		self.plotEvent.clear()
		

		self.radio.setup(params,self.plotEvent)
		self.view.canvas.initPlot(np.linspace(params['centerFrequency']-params['bandwidth']/2,params['centerFrequency']+params['bandwidth']/2,params['fftsize']),np.zeros(params['fftsize']))


		task1 = Worker(self.radio.stream,self.dataqueue,params['fftsize'],params['window'],0.3)
		task2 = Worker(self.view.canvas.updatePlot,self.dataqueue)

		self.threadpool.start(task1)
		self.threadpool.start(task2)


	def record(self,params,id):
		""" method for recording"""
		if not self.plotEvent.is_set():
			self.plotEvent.set()
		self.threadpool.waitForDone()
		self.plotEvent.clear()
		if id == 'VIEW':
			self.textUpdate.append('[VIEW] Recording requested.')
			filename =  'data/static/capture.bin'
			self.radio.setup(params,self.plotEvent)
			try:
				self.radio.record(filename,int(params['recordTime']*params['bandwidth']))
				self.textUpdate.append('[VIEW] Recording finished. Data Saved to:{}'.format(filename))
			except Exception:
				self.textUpdate.append('[VIEW] Overflow occured. Captured data may not be valid: {}'.format(filename))
			self.plot(params)
		if id == 'MAP':
			self.textUpdate.append('[MAP] Recording requested.')
			lat = params['position'][0]
			lng = params['position'][1]
			filename = 'data/geo/lat_'+ str(lat) + 'lng_' + str(lng) + '.bin'
			self.radio.setup(params,self.plotEvent)
			try:
				self.radio.record(filename,int(params['recordTime']*params['bandwidth']))
				self.textUpdate.append('[MAP] Recording finished. Data Saved to:{}'.format(filename))
			except Exception:
				self.textUpdate.append('[MAP] Overflow occured. Captured data may not be valid: {}'.format(filename))

			
		if id == 'GRID':
			self.textUpdate.append('[GRID] Recording requested.')
			x = params['position'][0]
			y = params['position'][1]
			step = min(params['step'])
			filename = 'data/grid/x_'+str(x) + 'y_' + str(y) + '.bin'
			self.radio.setup(params,self.plotEvent)
			try:
				self.radio.record(filename,int(params['recordTime']*params['bandwidth']))
				self.textUpdate.append('[GRID] Recording finished. Data Saved to:{}'.format(filename))
			except Exception:
				self.textUpdate.append('[GRID] Overflow occured. Captured data may not be valid: {}'.format(filename))
			task = Worker(self.grid.canvas.updatePlot,x,y,step,params['recordTime'],params['bandwidth'],filename)
			self.threadpool.start(task)


	def closeEvent(self,event):
		""" To handle the event close"""
		event.ignore()
		self.plotEvent.set()
		self.threadpool.waitForDone()
		event.accept()




if __name__ == '__main__':
	app = QApplication([])
	m = MainWindow()
	m.show()
	app.exec_()
