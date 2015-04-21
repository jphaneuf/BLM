from neo import io
import os
import numpy as np
from matplotlib import pylab
#10mV/pA
class dataManager:
	def __init__(self):
        	self.combinedSignal = np.array([])#combined raw signals
		self.combinedConductance = np.array([])#combined Conductance
		self.timeVector = np.array([])
        	self.threshold = 0
	def updateCombinedSignal(self,listOfFiles):
		self.combinedSignal = np.array([])#clear
		for abfFile in listOfFiles:
			print str(abfFile)
			x = io.AxonIO(str(abfFile))
			blks = x.read()
			signal = blks[0].segments[0].analogsignals[0]
			s = np.array(signal.segment.analogsignals[0])
			#pA/mV => nSiemens
			self.combinedSignal = np.concatenate([self.combinedSignal,s])			 
			self.samplePeriod = signal.sampling_period
		##This data set is huge.  Just throw away some of it for now
		reduction = 100
		self.combinedSignalReduced = self.combinedSignal[1::reduction]
		self.timeVector = np.array(range(len(self.combinedSignalReduced)))*self.samplePeriod*reduction		
	def filterSignal(self):
		self.combinedSignal = np.abs(self.combinedSignal)
	def integrateSignal(self):
		pass
	def computeFinalIntegral(self,timeStamps):
		"""time stamps for baseline grabs and integral windows are used
		to compute the final integral.  These values are grabbed from matplotlib figure.
		Includes applied voltage entry from user input dialog box"""
		noiseThreshold = 0.5#Threshold for integration,in nSiemens 
		totalIntegral = 0
		for windowSet in timeStamps:
			print "time stamps:",windowSet
			it1,it2,ib,av = [int(x/self.samplePeriod) for x in windowSet] #indices for baselineand integrals
			av = windowSet[3] #applied voltge in mV			
			print "indices:",it1,it2,ib
			print "applied Voltage:", av
			it1,it2 = sorted([it1,it2])#make sure it2>it1
			#get baseline Conductance @ index
			baselineConductance = np.mean(self.combinedSignal[max(ib-10,0):min(ib+10,len(self.combinedSignal))])/av
			integral = self.combinedSignal[it1:it2]/av- baselineConductance
			#pylab.plot(integral)
			#pylab.show()
			integral = [i if i > noiseThreshold else 0 for i in integral] # Clip all below noise
			integral = np.sum(integral)*self.samplePeriod
			totalIntegral += float(integral)
			print "window Integral:",integral
		print totalIntegral
		return totalIntegral

if __name__ == "__main__":
	dm = dataManager()
	#dm.updateCombinedSignal(["/home/joe/knowledge/blm/BLM Membrane Example/Recording 2, 50Hz lowpass.abf"])
	#dm.updateCombinedSignal(["C:\Users\jphaneuf\Downloads\Recording 1.abf"]) 
	dm.updateCombinedSignal(["C:\Users/joe/knowledge/blm/BLM Membrane Example/Recording 1, 50Hz lowpass.abf"]) 
