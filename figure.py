from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import Slider,Button,RectangleSelector
import matplotlib.text as mtext
import sys
from matplotlib.axes import Axes as mpAx
import numpy as np
from PyQt4 import QtGui,QtCore


class sAx(mpAx):
	##Slider axis: joins slider and axis into one
	dataLength = 10
	xlimMax= 10
	xpos,ypos,width,height = 0.25,0,0.65,0.03
	def __init__(self,fig,y,sName,sFunction):
		mpAx.__init__(self,fig,rect=(self.xpos,y,self.width,self.height))
		self.slider = Slider(self,sName,0,100,0)
		self.slider.on_changed(sFunction)
	def gi(self): # get Index
		return int(self.slider.val*self.dataLength/100)
	def gv(self):
		return self.slider.val*self.xlimMax/100
class integralWindow:
	###has baseline, integral windows
	def __init__(self,axes,appliedVoltage):
		self.axes = axes
		self.appliedVoltage = appliedVoltage
		self.indices = {"i1":0,"i2":0,"blg":0}
		self.lines = {}
		self.lines["i1"] = axes.axvline(x=1.4,color="red")
		self.lines["i2"] = axes.axvline(x=1.5,color="red")
		self.lines["blg"] = axes.axvline(x=1.6,color="green")#baselinegrabber
		for l in self.lines.values():
			l.set_xdata(0)
	def unHighlight(self):
		self.lines["i1"].set_color("sienna")
		self.lines["i2"].set_color("sienna")
		self.lines["blg"].set_color("darkslategray")
	def highlight(self):
		self.lines["i1"].set_color("red")
		self.lines["i2"].set_color("red")
		self.lines["blg"].set_color("green")
	def getTimes(self): #get all timeStamps
		return [self.lines["i1"].get_xdata(),
				self.lines["i2"].get_xdata(),
				self.lines["blg"].get_xdata(),
				self.appliedVoltage]
	def kill(self):
		self.lines["i1"].remove()
		self.lines["i2"].remove()
		self.lines["blg"].remove()
class integralWindowManager:
	def __init__(self,axes,textAxis,nbAxis,timeDeltaAxis,mainWidget):
		self.mainWidget = mainWidget #main Gui Widget, need for popup box
		self.axes = axes
		self.iws = []#[integralWindow(self.axes)]#integral windows
		self.selectedWindow = -1
		self.selectedBlineText = textAxis.text(0.2,0.075,str(0))
		self.nWindowsText = nbAxis.text(0,0.075,"windows")
		self.integralWindowText = timeDeltaAxis.text(0.2,0.075,"i window")
		#self.updateText()
	def highlightWindow(self,w):
		for lineSet in self.iws:
			lineSet.unHighlight()
		self.iws[w].highlight()
	def updateText(self):
		self.selectedBlineText.set_text(str(self.selectedWindow+1))
		self.nWindowsText.set_text("of "+str(len(self.iws)) +" windows")
		l = self.iws[self.selectedWindow].lines
		integralTimeDelta =  str(float(abs(l["i1"].get_xdata()-l["i2"].get_xdata())))
		self.integralWindowText.set_text("Integral dT:"+integralTimeDelta+"s")
	def nextWindow(self,v=0):
		self.selectedWindow +=1
		if self.selectedWindow > len(self.iws)-1:
			appliedVoltage,ok = QtGui.QInputDialog.getText(self.mainWidget,"Input Dialog","Enter Applied Voltage (mV):")
			self.iws.append(integralWindow(self.axes,float(appliedVoltage)))
		self.updateText()
		self.highlightWindow(self.selectedWindow)
	def prevWindow(self,v=0):
		self.selectedWindow = self.selectedWindow-1 if self.selectedWindow >0 else 0
		self.updateText()
		self.highlightWindow(self.selectedWindow)
	def setVLines(self,tmin,tmax,tbl):
		self.iws[self.selectedWindow].lines["i1"].set_xdata(tmin)
		self.iws[self.selectedWindow].lines["i2"].set_xdata(tmax)
		self.iws[self.selectedWindow].lines["blg"].set_xdata(tbl)
		self.updateText()
	def getBaselineTime(self):
		return self.iws[self.selectedWindow].lines["blg"].get_xdata()
	def getTimes(self):
		timeStamps = []
		for windowSet in self.iws:
			print windowSet
			timeStamps.append(windowSet.getTimes())
		return timeStamps
	def removeWindow(self,x):
		if self.iws:
			self.iws[self.selectedWindow].kill()
			self.iws.pop(self.selectedWindow)
			self.selectedWindow = min(self.selectedWindow,len(self.iws)-1)
			self.updateText()
class mplCanvas(FigureCanvas):
	def __init__(self,mainWidget):
		self.fig = Figure()
		self.mainWidget = mainWidget
		#fig,self.axes = plt.subplots()
		FigureCanvas.__init__(self,self.fig)
		self.axes = self.fig.add_subplot(111)
		self.axes.set_xlabel("Time(seconds)")
		self.axes.set_ylabel("pA")
		self.fig.subplots_adjust(left=0.1, bottom=0.4)
		self.l, = self.axes.plot(range(10),range(10,20))
		self.i1 = self.axes.axvline(x=0,color="red") #integral marker 1
		self.i2 = self.axes.axvline(x=0,color="red") #integral marker 2
		self.baseLineGrabber = self.axes.axvline(x=0,color="green") #where to get baseline average
		self.axes.hold(False)
		self.createSliders()
		self.createBaselineControls()
		self.dataLength = 10
		self.iText = self.fig.text(0.12,0.8,"Integral:0")
		self.yZoomSelector = RectangleSelector(self.axes, self.yZoom, drawtype='line')
	def yZoom(self,eclick, erelease):
		if eclick.button == 1: #left mouse
			ymin,ymax = sorted([eclick.ydata,erelease.ydata])
			self.axes.set_ylim(ymin,ymax)
			self.updatePlot()
		elif eclick.button == 3:#right mouse
			self.updateXlim(0)#pull xlim from sliders, resets
			#ylim to full zoomed out in the process
	def createBaselineControls(self):
		self.bax1 = mpAx(self.fig,rect=(0.15,0.14,0.1,0.03))#button axes
		self.fig.add_axes(self.bax1)
		self.butt1 = Button(self.bax1,'+')	
		self.bax2 = mpAx(self.fig,rect=(0.25,0.14,0.1,0.03))
		self.fig.add_axes(self.bax2)
		self.butt2 = Button(self.bax2,'-')	
		self.bax3 = mpAx(self.fig,rect=(0.35,0.14,0.1,0.03))
		self.fig.add_axes(self.bax3)
		self.bax3.set_axis_off()
		self.bax4 = mpAx(self.fig,rect=(0.05,0.14,0.1,0.03))
		self.fig.add_axes(self.bax4)
		self.removeButton = Button(self.bax4,'rmv')
		self.nbax = mpAx(self.fig,rect=(0.45,0.14,0.1,0.03))# number of windows
		self.fig.add_axes(self.nbax)
		self.nbax.set_axis_off()
		self.dt = mpAx(self.fig,rect=(0.6,0.14,0.1,0.03))#delta t
		self.fig.add_axes(self.dt)
		self.dt.set_axis_off()
		self.bmean = mpAx(self.fig,rect=(0.55,0.2,0.1,0.03))# #baseline
		self.fig.add_axes(self.bmean)
		self.bmean.set_axis_off()
		self.intTotal = mpAx(self.fig,rect=(0.1,0.2,0.1,0.03))# #baseline
		self.fig.add_axes(self.intTotal)
		self.intTotal.set_axis_off()
		self.baselineValueText = self.bmean.text(0,0,"baseline")
		self.integralTotalText = self.intTotal.text(0,0,"integral Total")
		self.iwm = integralWindowManager(self.axes,self.bax3,self.nbax,self.dt,self.mainWidget)
		self.butt1.on_clicked(self.iwm.nextWindow)
		self.butt2.on_clicked(self.iwm.prevWindow)
		self.removeButton.on_clicked(self.iwm.removeWindow)
	def createSliders(self):	
		self.sax1 = sAx(self.fig,0.1,"tmin %",self.updateXlim)
		self.fig.add_axes(self.sax1)	
		self.sax2 = sAx(self.fig,0.075,"tmax %",self.updateXlim)
		self.fig.add_axes(self.sax2)	
		self.sax3 = sAx(self.fig,0.05,"get Baseline",self.calculateBaseline)
		self.fig.add_axes(self.sax3)
		self.sax4 = sAx(self.fig,0.025,"integral min",self.integrateData)
		self.fig.add_axes(self.sax4)
		self.sax5 = sAx(self.fig,0.0,"integral max",self.integrateData)
		self.fig.add_axes(self.sax5)
	def calculateBaseline(self,value):
		baselineTime = self.iwm.getBaselineTime()
		baselineIndex = int(baselineTime/self.timeSlice)
		baselineMin,baselineMax = [max(baselineIndex-5,0),min(baselineIndex+5,self.dataLength-1)]
		baselineValue = np.mean(self.l.get_ydata()[baselineMin:baselineMax])
		self.baselineValueText.set_text("baseline:"+ str(baselineValue)+"pA")
		
		"""
		self.baseLineGrabber.set_xdata(self.sax3.gv())
		whereAt = self.sax3.gi()
		self.baseLine = np.mean(self.l.get_ydata()[whereAt-5:whereAt])
		"""
		#self.nWindowsText = nbAxis.text(0,0.075,"windows")
		#self
		self.integrateData()
	def updateXlim(self,sliderValue):
		self.axes.set_xlim(sorted([self.sax1.gv(),self.sax2.gv()]))
		try:
			xmin,xmax = sorted([self.sax1.gi(),self.sax2.gi()])		
			ymin = min(self.l.get_ydata()[xmin:xmax])
			ymax = max(self.l.get_ydata()[xmin:xmax])
			padding = 0.1*(ymax - ymin)
			self.axes.set_ylim(ymin-padding,ymax+padding)
		except:
			pass
		self.updatePlot()
	def updateData(self,xd,yd):
		self.dataLength = len(xd)
		print self.dataLength
		self.l.set_ydata(yd)
    		self.l.set_xdata(xd)
		self.axes.set_ylim(min(yd)-10,max(yd)+2)
		##Set slider class variables
		sAx.dataLength= self.dataLength
		sAx.xlimMax = np.max(self.l.get_xdata())
		self.updatePlot()
		self.timeSlice = self.l.get_xdata()[1]-self.l.get_xdata()[0]
	def updatePlot(self,**kwargs):
		self.axes.relim()
		self.axes.autoscale_view(scalex=False)
		#self.draw()
		self.fig.canvas.draw()
	def integrateData(self,sliderValue=None):
		#self.integralTotalText = self.intTotal.text(0,0,"integral Total")
		t1,t2 = sorted([self.sax4.gv(),self.sax5.gv()])
		tbl = self.sax3.gv()
		self.iwm.setVLines(t1,t2,tbl)
		integral = 0
		for integralSet in self.iwm.getTimes():
			imin = int(integralSet[0]/self.timeSlice)
			imax = int(integralSet[1]/self.timeSlice)
			baselineTime = integralSet[2]
			baselineIndex = int(baselineTime/self.timeSlice)
			baselineMin,baselineMax = [max(baselineIndex-5,0),min(baselineIndex+5,self.dataLength-1)]
			baselineValue = np.mean(self.l.get_ydata()[baselineMin:baselineMax])			
			_ = self.l.get_ydata()[imin:imax]
			_ = np.array(_)-baselineValue
			_ = np.sum(_)*float(self.timeSlice)
			integral += abs(_)
		self.integralTotalText.set_text("total integral:"+str(integral)+"pA*Seconds")
		#self.i1.set_xdata(t1)
		#self.i2.set_xdata(t2)
"""		
		try:
			integral = 0
			imin,imax = sorted([self.sax4.gi(),self.sax5.gi()])
			timeSlice = self.l.get_xdata()[1]-self.l.get_xdata()[0]
			integral = self.l.get_ydata()[imin:imax]
			integral = np.array(integral)-self.baseLine
			integral = np.sum(integral)*timeSlice	
		except:
			pass
		self.iText.set_text("Integral:"+str(float(integral)))
		"""
##Test:
class App(QtGui.QApplication):
    def __init__(self, *args):
        QtGui.QApplication.__init__(self, *args)
        self.main = QtGui.QMainWindow()    
        self.main.show()
        mc = mplCanvas(self.main)
        mc.show()
        mc.updateData(range(10),range(50,60))
        mc.draw()
        self.connect(self, QtCore.SIGNAL("lastWindowClosed()"), self.byebye )

    def byebye( self ):
        self.exit(0)

def main(args):
    global app
    app = App(args)
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)

