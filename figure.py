from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import Slider,Button
import matplotlib.text as mtext
from matplotlib.axes import Axes as mpAx
import numpy as np

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
		self.iText = self.fig.text(0.12,0.8,"Integral:0")		
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
		self.baseLineGrabber.set_xdata(self.sax3.gv())
		whereAt = self.sax3.gi()
		self.baseLine = np.mean(self.l.get_ydata()[whereAt-5:whereAt])
		self.integrateData()
	def updateXlim(self,sliderValue):
		self.axes.set_xlim(sorted([self.sax1.gv(),self.sax2.gv()]))
		try:
			xmin,xmax = sorted([self.sax1.gi(),self.sax2.gi()])		
			ymin = min(self.l.get_ydata()[xmin:xmax])
			ymax = max(self.l.get_ydata()[xmin:xmax])		
			self.axes.set_ylim(ymin-10,ymax+2)
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
	def updatePlot(self,**kwargs):
		self.axes.relim()
		self.axes.autoscale_view(scalex=False)
		#self.draw()
		self.fig.canvas.draw()
	def integrateData(self,sliderValue=None):
		t1,t2 = sorted([self.sax4.gv(),self.sax5.gv()])
		self.i1.set_xdata(t1)
		self.i2.set_xdata(t2)
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
##Test:
if __name__ == "__main__":
    mc = mplCanvas()
    mc.show()
    mc.updateData(range(10),range(50,60))
    mc.draw()
				
