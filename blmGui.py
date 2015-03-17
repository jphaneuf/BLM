import sys
from PyQt4 import QtGui,QtCore

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
		self.clearButton = QtGui.QPushButton("Clear Files")
		self.addWidget(self.addButton)
		self.addWidget(self.clearButton)
		self.files = []
		self.addButton.clicked.connect(self.addFile)
		self.clearButton.clicked.connect(self.removeFiles)
	def addFile(self):
		fileName = QtGui.QFileDialog.getOpenFileName(QtGui.QMainWindow(),'Open file','./')
		x = dataFile(fileName)
		x.pc.stateChanged.connect(self.createPlotList)
		self.addLayout(x)
		self.files.append(x)
	def removeFiles(self):
		self.files = []
	def createPlotList(self):
		#create list of files selected for plotting
		print	[x.fileName for x in self.files if x.pc.isChecked()]
#class Example(QtGui.QMainWindow):
class Example(QtGui.QWidget):
	def __init__(self):
		super(Example,self).__init__()
		self.initUI()
	def initUI(self):
		#QtGui.QFileDialog.getOpenFileName(self,'Open file','./')
		fm = fileManager()
		hbox = QtGui.QHBoxLayout()
		hbox.addStretch(1)
		vbox=QtGui.QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(hbox)
		vbox.addLayout(fm)
		self.setLayout(vbox)
		self.setGeometry(300,300,350,150)
		self.setWindowTitle('Signal & slot')
		self.show()

def main():
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())	

if __name__ == '__main__':
	main()
