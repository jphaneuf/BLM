from neo import io
import os
import numpy as np
#10mV/pA
class dataManager:
	def __init__(self):
        	self.combinedSignal = np.array([])
		self.timeVector = np.array([])
        	self.threshold = 0
	def updateCombinedSignal(self,listOfFiles):
		self.combinedSignal = np.array([])
		for abfFile in listOfFiles:
			print str(abfFile)
			x = io.AxonIO(str(abfFile))
			blks = x.read()
			signal = blks[0].segments[0].analogsignals[0]
			s = np.array(signal.segment.analogsignals[0])
			self.combinedSignal = np.concatenate([self.combinedSignal,s])			 
			self.samplePeriod = signal.sampling_period
		##This data set is huge.  Just throw away some of it for now
		##Will devise smoothing/reduction method later
		reduction = 100
		self.combinedSignal = self.combinedSignal[1::reduction]
		self.timeVector = np.array(range(len(self.combinedSignal)))*self.samplePeriod*reduction		
#		self.filterSignal()
	def filterSignal(self):
		self.combinedSignal = np.abs(self.combinedSignal)
	def integrateSignal(self):
		pass
	def getBaseline(self):
		pass
	def getStartTime(self):
		pass
	def getThresholdReachedTime(self):
		pass
	def getElapsedTime(self):
		pass
if __name__ == "__main__":
	dm = dataManager()
	#dm.updateCombinedSignal(["/home/joe/knowledge/blm/BLM Membrane Example/Recording 2, 50Hz lowpass.abf"])
	dm.updateCombinedSignal(["C:\Users\jphaneuf\Downloads\Recording 1.abf"]) 
 
