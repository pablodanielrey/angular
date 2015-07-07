import inject, logging, json, sys, traceback


from network.actions import Enroll

from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor

#http://code.activestate.com/recipes/439358-twisted-from-blocking-functions-to-deferred-functi/
from twisted.internet.threads import deferToThread
deferred = deferToThread.__get__



from model.config import Config
from model.utils import DateTimeEncoder

from model.exceptions import *


from model.session import Session





''' aca se definen las acciones a ser manejadas por el server de websocket '''

actions = [
    Enroll()
]



""" la transformo en un deferred para que sea procesada en otro thread """
@deferred
def dispatch(protocol,message):
    protocol.dispatch(message)

def sendMessage(protocol,message):
    protocol.sendMessage(message,False)


class ActionsServerProtocol(WebSocketServerProtocol):


    session = inject.attr(Session)


    def _encodeMessage(self,msg):
        jmsg = json.dumps(msg, ensure_ascii = False, cls=DateTimeEncoder)
        if (len(jmsg) < 1024):
            logging.debug(jmsg)

        ejmsg = jmsg.encode('utf-8')
        return ejmsg

    def _sendEncodedMessage(self,msg):
        if (len(msg) < 1024):
            logging.debug('server -> cliente {}'.format(msg))
        """ super(WebSocketServerProtocol,self).sendMessage(msg,False)"""
        reactor.callFromThread(sendMessage,super(WebSocketServerProtocol,self),msg)


    def sendException(self,e):
        msg = {'type':'Exception','name':e.__class__.__name__}
        self.sendMessage(msg)

    def sendError(self,msg,e):
        mmsg = {'id':msg['id'],'error':e.__class__.__name__}
        self.sendMessage(mmsg)


    def sendMessage(self,msg):
        ejmsg = self._encodeMessage(msg)
        self._sendEncodedMessage(ejmsg)

    def broadcast(self,msg):
        msg = self._encodeMessage(msg)
        self.factory.broadcast(msg)




    def dispatch(self,message):
        managed = False
        for action in actions:
            logging.debug('ejecutando {}'.format(action))
            managed = action.handleAction(self,message)
            logging.debug('retorno {}'.format(managed))
            if managed:
                break

        logging.debug('finalinzando ejecucion')



    def onMessage(self, payload, isBinary):

        logging.debug('mensaje recibido')

        try:
            if isBinary:
                """ por ahora no manejo mensajes binarios """
                return

            msg = payload.decode('utf-8')

            if len(msg) < 1024:
                logging.debug('cliente -> server {}'.format(msg))

            message = json.loads(msg)

            if 'action' not in message:
                raise MalformedMessage()

            if 'id' not in message:
                raise MalformedMessage()

            if 'session' in message:
                sid = message['session']
                self.session.touch(sid)

            try:
                dispatch(self,message)

            except AccessDenied as e:
                print(e.__class__.__name__ + ' ' + str(e))
                traceback.print_exc()
                self.sendError(message,e)

            except Exception as e:
                print(e.__class__.__name__ + ' ' + str(e))
                traceback.print_exc()
                self.sendError(message,e)
                raise e

        except Exception as e:
            print(e.__class__.__name__ + ' ' + str(e))
            traceback.print_exc()
            self.sendException(e)


    """ cliente se conecta. -- parametro : autobahn.websocket.protocol.ConnectionRequest """
    def onConnect(self,cr):
        logging.debug('cliente conectado')
        logging.debug(cr)
        return None

    def onOpen(self):
        logging.debug('conexión establecida')
        self.factory.register(self)

    def onClose(self,wasClean, code, reason):
        logging.debug('cliente desconectado {0}, {1}, {2}'.format(wasClean,code,reason))

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)





class BroadcastServerFactory(WebSocketServerFactory):

    def __init__(self, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = []


    def _encodeMessage(self,msg):
        jmsg = json.dumps(msg, ensure_ascii = False, cls=DateTimeEncoder)
        if (len(jmsg) < 1024):
            logging.debug(jmsg)

        ejmsg = jmsg.encode('utf-8')
        return ejmsg


    def register(self, client):
        if client not in self.clients:
            logging.debug("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            logging.debug("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        logging.debug("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c._sendEncodedMessage(msg)
            logging.debug("message sent to {}".format(c.peer))



def getPort():
    config = inject.instance(Config)
    log.startLogging(sys.stdout)
    factory = BroadcastServerFactory()
    factory.protocol = ActionsServerProtocol
    port = reactor.listenTCP(int(config.configs['server_port']), factory=factory, interface=config.configs['server_ip'])
    return (reactor,port,factory)
