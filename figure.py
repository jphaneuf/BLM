from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import Slider,Button
import matplotlib.text as mtext
import numpy as np
class mplCanvas(FigureCanvas):
	def __init__(self):
		self.fig = Figure()
		#fig,self.axes = plt.subplots()
		FigureCanvas.__init__(self,self.fig)
		self.axes = self.fig.add_subplot(111)
		self.fig.subplots_adjust(left=0.1, bottom=0.25)
		self.l, = self.axes.plot(range(10),range(10,20))
		self.i1 = self.axes.axvline(x=0,color="red") #integral marker 1
		self.i2 = self.axes.axvline(x=0,color="red") #integral marker 2
		self.baseLineGrabber = self.axes.axvline(x=0,color="green") #where to get baseline average
		self.axes.hold(False)
		self.createSliders()
		self.dataLength = 10
		self.x1 = 0
		self.x2 = self.dataLength
		self.xlims = [0,0]
		self.iText = self.fig.text(0.12,0.8,"Integral:0")		
	def createSliders(self):
		self.sax1 = self.fig.add_axes(( 0.25,0.1,0.65,0.03))
		self.sax2 = self.fig.add_axes(( 0.25,0.075,0.65,0.03))
		self.sax3 = self.fig.add_axes(( 0.25,0.05,0.65,0.03))
		self.sax4 = self.fig.add_axes(( 0.25,0.025,0.65,0.03))
		self.sax5 = self.fig.add_axes(( 0.25,0,0.65,0.03))		
		self.stmin = Slider(self.sax1,'tmin %', 0, 100,valinit = 0)
		self.stmin.on_changed(self.updateX1)
		self.stmax = Slider(self.sax2,'tmax %', 0, 100,valinit = 0)
		self.stmax.on_changed(self.updateX2)
		self.sintmin = Slider(self.sax4,'integral min', 0, 100,valinit = 0.15)
		self.sintmin.on_changed(self.updateInt1)
		self.sintmax = Slider(self.sax5,'integral max', 0, 100,valinit = 0.15)
		self.sintmax.on_changed(self.updateInt2)
		self.sbase = Slider(self.sax3,'get Baseline',0,100,valinit=0)
		self.sbase.on_changed(self.calculateBaseline)
	def calculateBaseline(self,value):
		self.baseLineGrabber.set_xdata(value*self.xlimMax/100)
		whereAt = int(value*self.dataLength/100)
		self.baseLine = np.mean(self.l.get_ydata()[whereAt-5:whereAt])
		self.integrateData()
	def updateX1(self,value):
		self.x1 = value
		self.updateXlim()
	def updateX2(self,value):
		self.x2 = value
		self.updateXlim()
	def updateInt1(self,value): #Integral slider 1
		self.i1.set_xdata(value*self.xlimMax/100)
		self.integrateData()
	def updateInt2(self,value): #Integral slider 2
		self.i2.set_xdata(value*self.xlimMax/100)
		self.integrateData()
	def updateXlim(self):
		self.xlimMax = np.max(self.l.get_xdata())
		self.xlims = sorted([self.x1*self.xlimMax/100,self.x2*self.xlimMax/100])		
		self.axes.set_xlim(self.xlims)
		xslices = sorted([self.x1*self.dataLength/100,self.x2*self.dataLength/100])		
		try:
			ymin = min(self.l.get_ydata()[int(self.xslices[0]):int(self.xslices[1])])
			ymax = max(self.l.get_ydata()[int(self.xslices[0]):int(self.xslices[1])])		
			self.axes.set_ylim(ymin-10,ymax+2)
			print "ylimits" ,ymin,ymax
		except:
			pass	
		self.updatePlot()
	def updateData(self,xd,yd):
		self.dataLength = len(xd)
		print self.dataLength
		self.l.set_ydata(yd)
    		self.l.set_xdata(xd)
		self.axes.set_ylim(min(yd)-10,max(yd)+2)
		self.updatePlot()
	def updatePlot(self,**kwargs):
		self.axes.relim()
		self.axes.autoscale_view(scalex=False)
		#self.axes.set_xlim(100)
		#self.draw()
		self.fig.canvas.draw()
	def integrateData(self):
		integral = 0
		try:
			integralMinIndex = int(self.sintmin.val*self.dataLength/100)
			integralMaxIndex = int(self.sintmax.val*self.dataLength/100)
			timeSlice = self.l.get_xdata()[1]-self.l.get_xdata()[0]
			integral = self.l.get_ydata()[integralMinIndex:integralMaxIndex] 
			integral = np.array(integral)-self.baseLine
			integral = np.sum(integral)*timeSlice	
			#integral = timeSlice*np.array(sum(self.l.get_ydata()[integralMinIndex:integralMaxIndex]))
		except:
			pass
		self.iText.set_text("Integral:"+str(float(integral)))
##Test:
if __name__ == "__main__":
    mc = mplCanvas()
    mc.show()
    mc.updateData(range(10),range(50,60))
    mc.draw()

