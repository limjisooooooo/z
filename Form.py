import sys
import json
import re
from packet import *
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
		r = re.compile("{'srcaddr':.+?, 'srcid':.+?, 'dstaddr':.+?, 'dstid':.+?, 'status':.+?, 's':.+?}")
		buf = str()
		while True:					
			while r.search(buf) == None:
				buf += self.parent.sock.recv(1024).decode()
				print(buf)
			#print("pass?")
			msg = r.search(buf).group()
			md = literal_eval(msg)			
			buf = buf[r.search(buf).end():]
			if md['status'] == "False":	
				#print("pass2?")
				break				
			elif md['status'] == 'connect':
				self.parent.model.appendRow(QStandardItem(md['s']))
				self.parent.listView.setModel(self.parent.model)	
				self.parent.textW.append("Enter. " + md['s'] )
			elif md['status'] == 'disconnect':
				#print(self.parent.model.findItems(md['s'])[0].row())					
				self.parent.model.removeRow(self.parent.model.findItems(md['s'])[0].row())
				self.parent.textW.append("Leave. " + md['s'] )						
			elif md['status'] == 'text':
				self.parent.textW.append("From. " + md['srcid'] + " : " + md['s'])										
			self.parent.bar.setValue(self.parent.bar.maximum())
			self.parent.textW.viewport().update()
				
		self.parent.err.showMessage(md['s'])
		self.parent.err.accepted.connect(self.parent.close)
		
		#self.close()
		#											
					
					
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

		self.err = QErrorMessage(self)
		
		self.setGeometry(300, 200, 624, 482)		
		self.setFixedSize(624, 482)
		self.setWindowTitle('Chat')
		self.show()
		
		self.lineEdit.returnPressed.connect(self.send)		
		self.model = QStandardItemModel()		
		
		self.sock = socket()
		self.sock.connect(('127.0.0.1', 1036))
		
		self.p = Packet('', self.id, 'BroadCast', 'BroadCast', 'connect', self.id)
		self.sock.sendall(self.p.DictoS().encode())
		
		#global r
		#buf = str()
		#while r.search(buf) == None:
		#	buf += self.sock.recv(1024).decode()
		#msg = r.search(buf).group()
		#md = literal_eval(msg)
		#buf = buf[r.search(buf).end():]		

		self.rec = Receive(self)
		self.rec.start()
		
	def send(self):
		if self.listView.selectedIndexes():
			p = Packet('', self.id, '', self.model.itemData(self.listView.selectedIndexes()[0])[0], 'text', self.lineEdit.text())
			self.sock.sendall(p.DictoS().encode())
			self.textW.append("To. " + self.model.itemData(self.listView.selectedIndexes()[0])[0] + " : " + self.lineEdit.text())
		else:
			p = Packet('', self.id, 'BroadCast', 'BroadCast', 'text', self.lineEdit.text())
			self.sock.sendall(p.DictoS().encode())
			self.textW.append("To. All User : " + self.lineEdit.text())
		self.bar.setValue(self.bar.maximum())
		self.lineEdit.setText("")		

if __name__ == '__main__':
	app = QApplication(sys.argv)	
	w = Form()
	sys.exit(app.exec())