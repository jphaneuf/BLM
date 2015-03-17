from neo import io
import os
import numpy as np

##load datasets
blmPath = "/home/joe/knowledge/blm/BLM Membrane Example"
blmFiles = os.listdir(blmPath)
r1dFile = blmPath+"/"+blmFiles[1]

x = io.AxonIO(r1dFile)
blks = x.read()
signal = blks[0].segments[0].analogsignals[0]
s = np.array(signal.segment.analogsignals[0])
#10mV/pA
##select datasets
##add
##plot/don't plot
##remove

#Enter threshold

##total dataset

#abs()
##filter
##integrate
#extract baseline

#print start time
#time @ threshold reached
#Elapsed Time

#class dataset


class dataManager:
    def __init__(self):
        self.combinedSignal = np.array([])
        self.threshold = 0
    def updateCombinedSignal(self,listOfFiles):
        pass
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
c = dataManager