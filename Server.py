from socket import *

def Server():	
	con, caddr = sock.accept()
	print('accept')
	while True:
		msg = con.recv(1024).decode()
		if not msg:
			break
		print(msg)
		msg = input('Msg : ')
		con.sendall(msg.encode())
		
HOST = ''
PORT = 8080
BUFSIZE = 1024
ADDR = (HOST, PORT)

sock = socket()

sock.bind(ADDR)
print('bind')
sock.listen(2)
print('listen')
while True:	
	Server()

con.close()