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
	def updateCombinedSignal(self,listOfFiles,listOfVoltages):
		self.combinedSignal = np.array([])
		self.combinedConductance = np.array([])
		print listOfVoltages
		for abfFile,v in zip(listOfFiles,listOfVoltages):
			print str(abfFile)
			x = io.AxonIO(str(abfFile))
			blks = x.read()
			signal = blks[0].segments[0].analogsignals[0]
			s = np.array(signal.segment.analogsignals[0])
			c = s/float(v)#convert to conductance using user input value for data set
			#Note: raw signal in pA,user input applied voltage is in mV 
			#pA/mV => nSiemens
			self.combinedSignal = np.concatenate([self.combinedSignal,s])			 
			self.combinedConductance = np.concatenate([self.combinedConductance,c])
			self.samplePeriod = signal.sampling_period
		##This data set is huge.  Just throw away some of it for now
		reduction = 100
		self.combinedSignal = self.combinedSignal[1::reduction]
		self.timeVector = np.array(range(len(self.combinedSignal)))*self.samplePeriod*reduction		
	def filterSignal(self):
		self.combinedSignal = np.abs(self.combinedSignal)
	def integrateSignal(self):
		pass
	def computeFinalIntegral(self,timeStamps):
		"""time stamps for baseline grabs and integral windows are used
		to compute the final integral.  These values are grabbed from matplotlib figure"""
		noiseThreshold = 3#Threshold for integration,in nSiemens 
		totalIntegral = 0
		for windowSet in timeStamps:
			print "time stamps:",windowSet
			it1,it2,ib = [int(x/self.samplePeriod) for x in windowSet] #indices for baselineand integrals
			print "indices:",it1,it2,ib
			it1,it2 = sorted([it1,it2])#make sure it2>it1
			#get baseline Conductance @ index
			baselineConductance = np.mean(self.combinedConductance[max(ib-10,0):min(ib+10,len(self.combinedConductance))])
			integral = self.combinedConductance[it1:it2]# - baselineConductance
#			pylab.plot(integral)
#			pylab.show()
			integral = [i if i > noiseThreshold else 0 for i in integral]
			integral = np.sum(integral)*self.samplePeriod
			totalIntegral += float(integral)
		print totalIntegral
		return totalIntegral

if __name__ == "__main__":
	dm = dataManager()
	#dm.updateCombinedSignal(["/home/joe/knowledge/blm/BLM Membrane Example/Recording 2, 50Hz lowpass.abf"])
	#dm.updateCombinedSignal(["C:\Users\jphaneuf\Downloads\Recording 1.abf"]) 
	dm.updateCombinedSignal(["C:\Users/joe/knowledge/blm/BLM Membrane Example/Recording 1, 50Hz lowpass.abf"]) 
