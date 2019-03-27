import ast

class Packet:
	def __init__(self, srcaddr = None, srcid = None, dstaddr = None, dstid = None, s = None, font = None, fcolor = None, status = None, str = None):
		self.pd = dict()		
		self.pd['srcaddr'] = srcaddr
		self.pd['srcid'] = srcid
		self.pd['dstaddr'] = dstaddr
		self.pd['dstid'] = dstid		
		self.pd['s'] = s
		self.pd['font'] = font
		self.pd['fcolor'] = fcolor
		self.pd['status'] = status
		self.str = str
	def StoDic(self):
		return literal_eval(self.pd)
	def DictoS(self):
		return str(self.pd)
	def setSrcaddr(self, srcaddr):
		self.pd['srcaddr'] = srcaddr
	def setSrcid(self, srcid):
		self.pd['srcid'] = srcid
	def setDstaddr(self, dstaddr):
		self.pd['dstaddr'] = dstaddr
	def setDstid(self, dstid):
		self.pd['dstid'] = dstid		
	def setS(self, s):
		self.pd['s'] = s	
	def setfont(self, font):
		self.pd['font'] = font
	def setfcolr(self, fcolor):
		self.pd['fcolor'] = fcolor
	def setStatus(self, status):
		self.pd['status'] = status

		
	
	
	
	