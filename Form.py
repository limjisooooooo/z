import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
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
				if k == 'connect':
					self.parent.model.appendRow(QStandardItem(str(v)))
					self.parent.listView.setModel(self.parent.model)	
				elif k == 'disconnect':
					print(self.parent.model.findItems(str(v))[0].row())					
					self.parent.model.removeRow(self.parent.model.findItems(str(v))[0].row())
					
				else:
					self.parent.textW.append("From. " + str(k) + " : " + v)										
					sleep(0.01)
					self.parent.bar.setValue(self.parent.bar.maximum())
					self.parent.textW.viewport().update()
					
					
					
class Enter(QDialog):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		#self.setGeometry(300, 200, 150, 30)
		
		self.txtName = QLineEdit(self)
		self.txtName.setGeometry(20, 10, 100, 20)

		self.btnOk = QPushButton(self)
		self.btnOk.setGeometry(130, 10, 50, 20)
		self.btnOk.setText("Enter")
		self.show()
		self.btnOk.clicked.connect(self.Enter_Form)
	
	def Enter_Form(self):
		self.parent.id = self.txtName.text()
		self.parent.__Main__Init__()
		self.close()
		
class Form(QMainWindow):
	def __init__(self):
		super().__init__()
		self.id = ""
		self.ent = Enter(self)
	
	def __Main__Init__(self):
		self.textW = QTextEdit(self)
		self.textW.setGeometry(0, 0, 471, 401)
		self.textW.setReadOnly(True)
		self.textW.setLineWrapMode(False)
		
		self.bar = QScrollBar(0x2, self)
		self.textW.setVerticalScrollBar(self.bar)
		
		self.lineEdit = QLineEdit(self)
		self.lineEdit.setGeometry(0, 410, 471, 31)
		
		self.listView = QListView(self)
		self.listView.setGeometry(480, 0, 141, 441)		
		
		self.setGeometry(300, 200, 624, 482)		
		self.setFixedSize(624, 482)
		self.setWindowTitle('Chat')
		self.show()
		
		self.lineEdit.returnPressed.connect(self.send)		
		self.model = QStandardItemModel()		
		
		self.sock = socket()
		self.sock.connect(('180.228.77.83', 8080))
		self.sock.sendall(self.id.encode())
		if self.sock.recv(1024).decode() == "False":
			self.err = QErrorMessage(self)
			self.err.showMessage("Id 중복 Error!")
			#self.close()
			self.err.accepted.connect(self.close)
		self.rec = Receive(self)
		self.rec.start()
		
	def send(self):
		if self.listView.selectedIndexes():			
			self.sock.sendall(("'" +self.model.itemData(self.listView.selectedIndexes()[0])[0] + "' : '" + self.lineEdit.text() + "'").encode())
			self.textW.append("To. " + self.model.itemData(self.listView.selectedIndexes()[0])[0] + " : " + self.lineEdit.text())
		else:
			self.sock.sendall(("'BroadCast' : '" + self.lineEdit.text() + "'").encode())
			self.textW.append("To. All User : " + self.lineEdit.text())
		self.bar.setValue(self.bar.maximum())
		self.lineEdit.setText("")		

if __name__ == '__main__':
	app = QApplication(sys.argv)	
	w = Form()
	sys.exit(app.exec())