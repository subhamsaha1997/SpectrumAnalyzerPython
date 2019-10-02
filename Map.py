
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os

class Mapview(QWidget):
	""" creates the map widget for the GPS view"""
	
	def __init__(self,parent = None):
		super(Mapview,self).__init__(parent)
		self.view = view = QWebEngineView()
		html = open('map.html','r').read()
		view.setHtml(html)
		view.loadFinished.connect(self.onLoadFinished)

		layout = QHBoxLayout()
		layout.addWidget(view)
		self.setLayout(layout)

	def onLoadFinished(self,status):
		if status:
			javascript = open('map.js','r').read()
			self.view.page().runJavaScript(javascript,self.ready)

	def ready(self,val):
		pass

	def addMarker(self,position):
		#get latitude and longitude from position tuple
		lat, lng = position
		# add marker using javascript function
		self.view.page().runJavaScript('onLocate({},{})'.format(lat,lng))




if __name__ == '__main__':
	app = QApplication([])
	m = Mapview()
	m.show()
	app.exec_()