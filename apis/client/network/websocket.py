# -*- coding: utf-8 -*-
import sys, inject, json, logging
import uuid

from model.config import Config
from model.utils import DateTimeEncoder

from twisted.python import log
from twisted.internet import reactor

from autobahn.twisted.websocket import WebSocketClientFactory
from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import connectWS




class MyWsClientProtocol(WebSocketClientProtocol):

    protocols = []
    callbacks = []

    @classmethod
    def addCallback(cls,callback):
        if callback not in cls.callbacks:
            cls.callbacks.append(callback)



    @classmethod
    def getProtocols(cls):
        return cls.protocols

    @classmethod
    def register(cls,instance):
        if instance not in cls.protocols:
            cls.protocols.append(instance)

    @classmethod
    def unregister(cls,instance):
        if instance in cls.protocols:
            cls.protocols.remove(instance)

    def __init__(self):
        logging.info('instanciando protocolo')
        super(WebSocketClientProtocol,self).__init__()
        self.messages = {}
        logging.info('protocolo instanciado')


    def onConnect(self, response):
        logging.info("Connected to Server: {}".format(response.peer))


    def onOpen(self):
        logging.debug('client connected to server')
        self.__class__.register(self)

        for c in self.__class__.callbacks:
            c(self)


    def onClose(self, wasClean, code, reason):
        self.messages = {}
        logging.debug('client disconnected from server')
        self.__class__.unregister(self)


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
                callback(self,message)
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

        ''' genero un id si no tiene '''
        if 'id' not in msg:
            msg['id'] = str(uuid.uuid4())

        self.messages[msg['id']] = callback
        emsg = self._encodeMessage(msg)
        self._sendEncodedMessage(emsg)


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

    try:
        config = inject.instance(Config)
        log.startLogging(sys.stdout)

        url = 'ws://{}:{}'.format(config.configs['server_ip'],config.configs['server_port'])
        logging.info('conectando a {}'.format(url))

        factory = WebSocketClientFactory(url=url,debug=False,debugCodePaths=False)
        factory.protocol = MyWsClientProtocol

        connectWS(factory)
        ''' reactor.connectTCP(config.configs['server_ip'], int(config.configs['server_port']), factory=factory) '''

        return reactor

    except Exception as e:
        logging.exception(e)
        raise e
