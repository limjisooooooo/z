from threading import *
from socket import *
from time import *
from ast import *

def Server(con, caddr):		
	#msg = dict()

	while True:		
		try:
			print("...Ing")
			msg = literal_eval("{" + con.recv(1024).decode()+ "}")						
			print(msg)
			for k, v in msg.items():
				print(k)
				d[k].sendall((str(caddr) + " : '" + v + "'").encode())
			#con.sendall(msg.encode())
		except:
			for c in d.values():
				try:
					c.sendall(("'disconnect' : " + str(caddr)).encode())
				except:
					break
			del d[caddr]
			break
		
	con.close()	
		
if __name__ == '__main__':	
	d = dict()
	HOST = ''
	PORT = 8080
	BUFSIZE = 1024
	ADDR = (HOST, PORT)
	sock = socket()
	sock.bind(ADDR)
	while True:
		sock.listen(1)
		con, caddr = sock.accept()
		for k in d.keys():
			con.sendall(("'connect' : " + str(k)).encode())
			sleep(0.01)
		d[caddr] = con
		for c in d.values():			
			c.sendall(("'connect' : " + str(caddr)).encode())
		print('connect')		
		t = Thread(target=Server, args=(con, caddr))		
		t.start()