from threading import *
from socket import *
from time import *
from ast import *

def Server(con, id):		
	#msg = dict()

	while True:		
		try:
			#print(msg)
			msg = literal_eval(con.recv(1024).decode())			
			for k, v in msg.items():
				if k == 'BroadCast':
					for ck, c in d.items():
						if ck == id :
							continue
						c.sendall(("{'" + id + "' : '" + v + "'}").encode())
				else:
					d[k].sendall(("{'" + id + "' : '" + v + "'}").encode())
			#con.sendall(msg.encode())
		except:
			for c in d.values():
				try:					
					c.sendall(("{'disconnect' : '" + id + "'}").encode())
				except:
					continue
			del d[id]
			break
		
	con.close()	
		
if __name__ == '__main__':	
	d = dict()
	HOST = ''
	PORT = 1036
	BUFSIZE = 1024
	ADDR = (HOST, PORT)
	sock = socket()
	sock.bind(ADDR)
	while True:
		sock.listen(1)
		con, caddr = sock.accept()
		id = con.recv(1024).decode()
		if id in d.keys():
			con.sendall("False".encode())
			con.close()
			continue
		con.sendall("True".encode())
			
		for k in d.keys():
			con.sendall(("{'connect' : '" + str(k) + "'}").encode())			
			
		d[id] = con
		
		for c in d.values():			
			c.sendall(("{'connect' : '" + id + "'}").encode())
		print('connect', con, id)		
		t = Thread(target=Server, args=(con, id))		
		t.start()