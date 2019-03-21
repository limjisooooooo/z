import sys
from PyQt5.QtWidgets import *
#from PyQt5.QtGui import *

class Form(QMainWindow):
	def __init__(self):
		super().__init__()
		self.show()
		self.setWindowTitle('Sample')
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = Form()
	sys.exit(app.exec())