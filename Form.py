import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from socket import *
from PyQt5.QtCore import QThread
from ast import *
from time import *


class Receive(QThread):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		
	def __del__(self):
		self.wait()
		
	def run(self):
		d = dict()
		while True:			
			d = literal_eval("{" + self.parent.sock.recv(1024).decode() + "}")
			for k, v in d.items():
				print(k, v)
				if k == 'connect':
					self.parent.model.appendRow(QStandardItem(str(v)))
					self.parent.ui.listView.setModel(self.parent.model)	
				elif k == 'disconnect':
					self.parent.model.removeRow(self.parent.model.findItems(str(v))[0].row())
					#print(self.parent.model.findItems(str(v))[0].row())
				else:
					self.parent.ui.textBrowser.append(str(k) + " 님의 말 : " + v)
class Form(QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = loadUi("Form.ui")		
		self.ui.show()
		self.ui.lineEdit.returnPressed.connect(self.send)
		self.ui.setWindowTitle('Chat')
		self.model = QStandardItemModel()		
		self.sock = socket()
		self.sock.connect(('127.0.0.1', 8080))
		self.rec = Receive(self)
		self.rec.start()		
	def send(self):
	#	print(self.model.itemData(self.ui.listView.selectedIndexes()[0]))
		print(self.model.itemData(self.ui.listView.selectedIndexes()[0])[0] + " : " + self.ui.lineEdit.text())
		self.sock.sendall((self.model.itemData(self.ui.listView.selectedIndexes()[0])[0] + " : '" + self.ui.lineEdit.text() + "'").encode())
	#	self.ui.textBrowser.append(self.ui.listView.selectedIndexes())
	#	self.sock.sendall(self.ui.lineEdit.text().encode())
		self.ui.textBrowser.append(self.ui.lineEdit.text())
		self.ui.lineEdit.setText("")
	
	def __del__(self):
		self.sock.close()
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = Form()
	sys.exit(app.exec())