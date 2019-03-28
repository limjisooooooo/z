import sys
import base64
from PyQt5.QtWidgets import *
#from PyQt5.QtGui import *

class Form(QMainWindow):
	def __init__(self):
		super().__init__()
		self.browser = QTextBrowser(self)
		self.browser.setGeometry(0, 0, 471, 401)
		self.setGeometry(0, 0, 500, 500)
		
		self.btnFile = QPushButton(self)
		self.btnFile.setGeometry(2, 430, 25, 25)
		self.btnFile.clicked.connect(self.fopen)
		self.show()
		self.setWindowTitle('Sample')
	def fopen(self):
		FileName, Filter = QFileDialog.getOpenFileUrl()		
		if FileName.path() != "":
			f = open(FileName.path()[1:], 'rb')
			data = base64.b64encode(f.read())
			#print(data)
			self.browser.append("<img src='data:image/jpeg;base64, " + data.decode() + "' alt='Image Can't Load'/>")
			f.close()
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = Form()
	sys.exit(app.exec())