from threading import *
from socket import *
from time import *
from ast import *

from packet import *
import re

def Server(con, caddr):		
	#msg = dict()	
	r = re.compile("{'srcaddr':.+?, 'srcid':.+?, 'dstaddr':.+?, 'dstid':.+?, 's':.+?, 'font':.+?, 'fcolor':.+?, 'status':.+?}")
	id = str()
	while True:		
		try:
			buf = str()			
			while r.search(buf) == None:
				buf += con.recv(1024).decode()
			msg = r.search(buf).group()
			md = literal_eval(msg)
			print(md)
			buf = buf[r.search(buf).end():]
			if md['status'] == 'connect':
				if md['s'] in idic.keys():					
					md['status'] = 'False'
					md['s'] = 'Id Duplicate Error'
					print(md)
					con.sendall(str(md).encode())
					break
				
				id = md['s']
				
				for c in d.values():					
					c.sendall(msg.encode())				
				
				d[caddr] = con
				#print(d[caddr])
				idic[id] = caddr
				#print(idic[id])
				
				for i in idic.keys():
					md['s'] = i
					con.sendall(str(md).encode())
				
			elif md['status'] == 'text':
				if md['dstid'] == 'BroadCast':
					for c in d.values():
						if c != con :							
							c.sendall(msg.encode())
				else:
					d[idic[md['dstid']]].sendall(msg.encode())

		except:
			#print("엥 왜 실행?")
			for c in d.values():
				try:
					p = Packet('', '', '', '', id, '', 0, 'disconnect') 
					c.sendall(p.DictoS().encode())
				except:
					continue
			del idic[id]
			#print(id)
			del d[caddr]
			break		
	con.close()	
		
if __name__ == '__main__':	
	d = dict()
	idic = dict()
	HOST = ''
	PORT = 1036
	BUFSIZE = 1024
	ADDR = (HOST, PORT)
	sock = socket()
	sock.bind(ADDR)
	while True:
		sock.listen(1)
		con, caddr = sock.accept()
		#id = con.recv(1024).decode()
		#if id in d.keys():
		#	con.sendall("False".encode())
		#	con.close()
		#	continue
		#con.sendall("True".encode())
			
		#for k in d.keys():
		#	con.sendall(("{'connect' : '" + str(k) + "'}").encode())			
			
		#d[caddr] = con
		
		#for c in d.values():			
		#	c.sendall(("{'connect' : '" + id + "'}").encode())
		#print('connect', con, id)		
		t = Thread(target=Server, args=(con, caddr))		
		t.start()