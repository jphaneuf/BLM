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
		import csv
		with open('/home/joe/knowledge/blm/eggs.csv', 'rb') as csvfile:
			spamreader = csv.reader(csvfile)
			self.combinedSignal= np.array([float(row[0]) for row in spamreader])
		"""		
		for abfFile in listOfFiles:
			print str(abfFile)
			x = io.AxonIO(str(abfFile))
			blks = x.read()
			signal = blks[0].segments[0].analogsignals[0]
			s = np.array(signal.segment.analogsignals[0])
			self.combinedSignal = np.concatenate([self.combinedSignal,s])			 
			self.samplePeriod = signal.sampling_period
		
		self.timeVector = np.array(range(len(self.combinedSignal)))*self.samplePeriod
		"""		
		self.timeVector = np.array(range(len(self.combinedSignal)))
		self.filterSignal()
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
	def getSubsetSignal(self,minmax):
		#take subset from sliders, and plot
		pmin = minmax[0] #% min
		pmax = minmax[1] #%		
		slength = len(self.combinedSignal)
		imin = np.round(pmin*slength/100)
		imax = np.round(pmax*slength/100)
		print pmin,pmax,slength,imin,imax
		return self.timeVector[imin:imax],self.combinedSignal[imin:imax]
if __name__ == "__main__":
	dm = dataManager()
	dm.updateCombinedSignal(["/home/joe/knowledge/blm/BLM Membrane Example/Recording 2, 50Hz lowpass.abf"])
