import json
import pylab
import traceback

from BITalino import *

from sys import exit
from txws import WebSocketFactory
from twisted.internet import protocol, reactor

def tostring(data):
    dtype=type(data).__name__
    if dtype=='ndarray':
        if pylab.shape(data)!=(): data=list(data)
        else: data='"'+data.tostring()+'"'
    elif dtype=='dict' or dtype=='tuple':
        try: data=json.dumps(data)#'"'+unicode(data)+'"'
        except: pass
    elif dtype=='NoneType':
        data=''
    elif dtype=='str' or dtype=='unicode':
        data=json.dumps(data)#'"'+unicode(data)+'"'
    
    return str(data)

class VS(protocol.Protocol):
	def connectionMade(self):
		print "CONNECTED"
		self.transport.write('server.connected()')

	def send(self,data,prot):
		prot.transport.write(data)

	def dataReceived(self, req):
		try:
			if not req.find('read'):
				print '> ' + req
			
			res = eval(req)
			
			if (req.find('shutdown')>=0):
				return
			
			li=req.find('(')
			li=li if li>=0 else None
			
			res=req[:li]+'('+tostring(res)+');'
			
			if not res.find('read'):
				print '< ' + res    
		except Exception as e:
			print traceback.format_exc()
			res='sys.exception("'+str(e)+'")'
			
		self.transport.write(res)
        
	def connectionLost(self, reason):
		server.shutdown()
		return


class server(object):
    @staticmethod
    def shutdown():
	    connector.stopListening()
	    try: reactor.stop()
	    except: pass

	    print "DISCONNECTED"

    
class VSFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return VS()


if __name__=='__main__':
	try:
		ip_addr, port = "127.0.0.1", 9001

		bitalino = BITalino()
		
		print "LISTENING AT %s:%s"%(ip_addr, port)
		
		connector = reactor.listenTCP(port, WebSocketFactory(VSFactory()))
		reactor.run()

	except Exception as e:
		print traceback.format_exc()
