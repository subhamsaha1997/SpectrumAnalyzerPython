from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np 
from Queue import Empty

class Toolbar(NavigationToolbar):
	""" Adds necessary tools in the toolbar"""

	def __init__(self,canvas_,parent = None):
		
		self.toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ('Pan','Zoom','Save')]
		super(Toolbar,self).__init__(canvas_,parent)
		


class Canvas3D(QWidget):
	""" Widget for plotting the signal"""

	def __init__(self,parent=None,width=6.4,height=4.8, dpi = 72):
		super(Canvas3D,self).__init__(parent)
		layout = QVBoxLayout()
		self.fig = FigureCanvas(Figure(figsize=(width,height)))
		self.axis = self.fig.figure.add_subplot(111,projection='3d')
		
		self.name = "Signal Strength Analysis"
		self.xname = "X-Position (m)"
		self.yname = "Y-Position (m)"
		self.zname = "Signal Strength"
		self.axis.set(title=self.name,xlabel=self.xname,ylabel=self.yname,zlabel=self.zname)
		
		layout.addWidget(self.fig)
		self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
		self.updateGeometry()
		layout.addWidget(Toolbar(self.fig,self))
		self.setLayout(layout)

	#initialize the plot
	def init(self,xsize,ysize):
		self.axis.set_xlim(0,xsize)
		self.axis.set_ylim(0,ysize)

	def updatePlot(self,x,y,step,duration,samplingFrequency,filename):
		e = self.calculateEnergy(filename,duration,samplingFrequency)
		print "Energy {}".format(e)
		self.axis.bar3d(x,y,0,step/10,step/10,e,'b',shade = True)
		self.fig.figure.canvas.flush_events()

	# update the plot
	def calculateEnergy(self,filename,duration,samplingFrequency):
		with open(filename,'rb') as fid:
			z = np.fromfile(fid,dtype=np.complex64)

			e = np.sum(np.abs(z)**2,axis=0)
			e = e*duration/samplingFrequency
			return e
