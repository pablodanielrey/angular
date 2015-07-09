# -*- coding: utf-8 -*-
import inject, json, logging

from model.utils import DateTimeEncoder

from twisted.python import log
from twisted.internet import reactor

from autobahn.twisted.websocket import WebSocketClientFactory
from autobahn.twisted.websocket import WebSocketClientProtocol




class MyClientProtocol(WebSocketClientProtocol):

    def __init__(self):
        super(WebSocketClientProtocol,self).__init__()
        self.messages = {}
        self.connected = False

    def onOpen(self):
        self.connected = True
        logging.debug('client connected to server')


    def onClose(self):
        self.connected = False
        self.messages = {}
        logging.debug('client disconnected from server')

    def isConnected(self):
        return self.connected


    def onMessage(self, payload, isBinary):
        msg = payload.decode('utf-8')

        if len(msg) < 1024:
            logging.debug('server -> client {}'.format(msg))

        message = json.loads(msg)

        if 'id' not in message:
            return
        id = message['id']
        found = False

        try:
            if id in self.messages.keys():
                found = True
                logging.debug('llamando a callback para el mensaje con id {}'.format(id))
                callback = self.messages[id]
                callback(message)
            else:
                logging.debug('No se encontro ningún callback para el mensaje con id {}'.format(id))

        except Exception as e:
            logging.exception(e)

        finally:
            if found:
                del self.messages[message['id']]




    def sendMessage(self,msg,callback):
        if not self.connected:
            raise Exception()

        self.messages[msg['id']] = callback
        emsj = self._encodeMessage(msg)
        self._sendEncodedMessage(msg)


    def _encodeMessage(self,msg):
        jmsg = json.dumps(msg, ensure_ascii = False, cls=DateTimeEncoder)
        if (len(jmsg) < 1024):
            logging.debug(jmsg)

        ejmsg = jmsg.encode('utf-8')
        return ejmsg

    def _sendEncodedMessage(self,msg):
        if (len(msg) < 1024):
            logging.debug('client -> server {}'.format(msg))
        super(WebSocketClientProtocol,self).sendMessage(msg,False)




def getReactor():
    config = inject.instance(Config)
    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory()
    factory.protocol = MyClientProtocol

    reactor.connectTCP(config.configs['server_ip'], int(config.configs['server_port']), factory=factory)
    return reactor
