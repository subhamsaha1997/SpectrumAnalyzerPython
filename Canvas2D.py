from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
from matplotlib.figure import Figure
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Queue import Empty


class Toolbar(NavigationToolbar):
	""" Adds necessary tools in the toolbar"""

	def __init__(self,canvas_,parent = None):
		
		self.toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ('Pan','Zoom','Save')]
		super(Toolbar,self).__init__(canvas_,parent)
		

class Canvas2D(QWidget):
	""" Widget for plotting the signal"""

	def __init__(self,parent=None,width=6.4,height=4.8,dpi=72):
		super(Canvas2D,self).__init__(parent)
		layout = QVBoxLayout()
		self.fig = FigureCanvas(Figure(figsize=(width,height)))
		self.axis = self.fig.figure.subplots()
		
		self.name = "Frequency Analysis"
		self.xname = "Frequency (Hz)"
		self.yname = "Magnitude"
		
		
		
		layout.addWidget(self.fig)
		self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
		self.updateGeometry()
		layout.addWidget(Toolbar(self.fig,self))
		self.setLayout(layout)

	#initialize the plot
	def initPlot(self,x,y):
		self.axis.clear()
		self.axis.set(title=self.name,xlabel=self.xname,ylabel=self.yname)
		self.axis.set_ylim(0,15)
		self.line, = self.axis.plot(x,y,'b')

	# update the plot
	def updatePlot(self,queue,timeout = 0.5):
		
		while True:
			try:
				data = queue.get(timeout=timeout)
				self.line.set_ydata(data)
				self.fig.figure.canvas.draw()
				self.fig.figure.canvas.flush_events()
		
			except Empty:
				print('TIMEOUT')
				break