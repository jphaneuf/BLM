import sys
from PyQt4 import QtGui,QtCore
from abfEda import dataManager
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from figure import mplCanvas

class comm(QtCore.QObject):
	updateDataTrigger = QtCore.pyqtSignal()
class dataFile(QtGui.QHBoxLayout):
	def __init__(self,fileName):
		super(dataFile,self).__init__()
		self.fileName = fileName
		self.addStretch(1)
		self.wg = QtGui.QWidget()
		self.lbl = QtGui.QLabel(fileName,self.wg)
		self.pc = QtGui.QCheckBox("yes",self.wg)		
		self.addWidget(self.lbl) 
		self.addWidget(self.pc)
class fileManager(QtGui.QVBoxLayout):
	def __init__(self):
		super(fileManager,self).__init__()
		self.addButton = QtGui.QPushButton("Add File")
		self.addWidget(self.addButton)
		self.files = []
		self.addButton.clicked.connect(self.addFile)
		self.c = comm()
	def addFile(self):
		fileName = QtGui.QFileDialog.getOpenFileName(QtGui.QMainWindow(),'Open file','./')
		x = dataFile(fileName)
		x.pc.stateChanged.connect(self.createPlotList)
		self.addLayout(x)
		self.files.append(x)
	def createPlotList(self):
		self.plotList = [x.fileName for x in self.files if x.pc.isChecked()]
		self.c.updateDataTrigger.emit()
class blmGui(QtGui.QWidget):
	def __init__(self):
		super(blmGui,self).__init__()
		self.initUI()
	def initUI(self):
		self.mpl = mplCanvas(self) #passes self as main widget, used for popup boxes
		self.fm = fileManager()
		self.dm = dataManager()
		self.fm.c.updateDataTrigger.connect(self.updateEverything)
		self.snapshotButton = QtGui.QPushButton("Save Figure")
		self.snapshotButton.clicked.connect(self.saveFigure)
		self.goButton = QtGui.QPushButton("Compute Final Integral")
		self.goButton.clicked.connect(self.computeFinalIntegral)
		self.totalIntegralLabel = QtGui.QLabel("Total Integral: 0nSiemen*Seconds",self)
		hbox = QtGui.QHBoxLayout()
		hbox.addStretch(1)
		vbox=QtGui.QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(hbox)
		vbox.addLayout(self.fm)
		vbox.addWidget(self.mpl)
		vbox.addWidget(self.snapshotButton)
		vbox.addWidget(self.goButton)
		vbox.addWidget(self.totalIntegralLabel)
		self.setLayout(vbox)
		self.setGeometry(300,300,700,500)
		self.setWindowTitle('BLM Analysis')
		self.show()
	def updateEverything(self):
		self.dm.updateCombinedSignal(self.fm.plotList)
		self.updatePlot()
	def updatePlot(self):
		self.mpl.updateData(self.dm.timeVector,self.dm.combinedSignal)
	def saveFigure(self):
		fileName = str(QtGui.QFileDialog.getSaveFileName(QtGui.QMainWindow(),'Save Figure As','./',filter='*.png'))
		self.mpl.fig.savefig(fileName)
	def computeFinalIntegral(self):
		totalIntegral = self.dm.computeFinalIntegral(self.mpl.iwm.getTimes())
		self.totalIntegralLabel.setText("Total Integral:"+str(totalIntegral)+" nSiemen*Seconds")
def main():
	app = QtGui.QApplication(sys.argv)
	ex = blmGui()
	sys.exit(app.exec_())	

if __name__ == '__main__':
	main()
