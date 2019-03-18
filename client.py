from socket import *

sock = socket()

sock.connect(('127.0.0.1', 8080))
while True:	
	msg = input('Msg : ')
	if not msg:
		break
	sock.sendall(msg.encode())
	#msg = sock.recv(1024).decode()
	print(msg)
sock.close()