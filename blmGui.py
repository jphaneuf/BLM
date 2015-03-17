import sys
from PyQt4 import QtGui,QtCore
#box: has filename, full file path,remove button,plotbutton
#add button

class dataFile(QtGui.QHBoxLayout):
	def __init__(self):
		super(dataFile,self).__init__()
		#text
		#check box
		self.rmButton = QtGui.QPushButton("rm")
		self.addWidget(self.rmButton)
class fileManager(QtGui.QVBoxLayout):
	def __init__(self):
		super(fileManager,self).__init__()
		self.addButton = QtGui.QPushButton("Add File")
		self.addWidget(self.addButton)
		myFile = dataFile()
		self.files = []
		self.addButton.clicked.connect(self.addFile)
	def addFile(self):
		x = dataFile()
		self.addLayout(x)
		self.files.append(x)
	
#fm = fileManager()
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
