from neo import io
import os
import numpy as np
#10mV/pA
class dataManager:
	def __init__(self):
        	self.combinedSignal = np.array([])
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
		print len(self.combinedSignal)
	def filterSignal(self):
		pass
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

