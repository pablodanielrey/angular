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
    eventHandlers = []

    @classmethod
    def addEventHandler(cls,callback):
        if callback not in cls.eventHandlers:
            cls.eventHandlers.append(callback)


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




    def _processMessage(self,message):
        id = message['id']
        found = False

        try:
            if id in self.messages.keys():
                found = True
                logging.debug('llamando a callback para el mensaje con id {}'.format(id))
                callback = self.messages[id]
                callback(self,message)
                logging.debug('callback retornada')
            else:
                logging.debug('No se encontro ningún callback para el mensaje con id {}'.format(id))

        except Exception as e:
            logging.exception(e)
            raise e

        finally:
            if found:
                del self.messages[message['id']]


    def _processEvent(self,message):
        e = None
        for eh in self.__class__.eventHandlers:
            try:
                eh(message)
            except Exception as ex:
                logging.exception(ex)
                e = ex
        if e:
            raise e


    def onMessage(self, payload, isBinary):
        msg = payload.decode('utf-8')

        if len(msg) < 1024:
            logging.debug('server -> client {}'.format(msg))

        message = json.loads(msg)

        try:
            if 'type' in message:
                self._processEvent(message)
                return

            if 'id' in message:
                self._processMessage(message)
                return

        except Exception as e:
            logging.exception(e)



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





class MyWebSocketClientFactory(WebSocketClientFactory):

    def __init__(self,myLifeCycleAdapter=None,url=None,debug=False,debugCodePaths=False):
        super(WebSocketClientFactory,self).__init__(url=url,debug=debug,debugCodePaths=debugCodePaths)
        self.myLifeCycleAdapter = myLifeCycleAdapter

    def clientConnectionFailed(self, connector, reason):
        super(WebSocketClientFactory,self).clientConnectionFailed(connector,reason)
        if self.myLifeCycleAdapter:
            myLifeCycleAdapter.clientConnectionFailed(self,connector,reason)




def getProtocol():
    return MyWsClientProtocol


def connectClient(myFactory=None):

    try:
        config = inject.instance(Config)
        log.startLogging(sys.stdout)

        url = 'ws://{}:{}'.format(config.configs['server_ip'],config.configs['server_port'])
        logging.info('conectando a {}'.format(url))

        factory = None
        if myFactory is None:
            factory = WebSocketClientFactory(url=url,debug=False,debugCodePaths=False)
        else:
            factory = myFactory

        factory.protocol = getProtocol()

        connectWS(factory)
        ''' reactor.connectTCP(config.configs['server_ip'], int(config.configs['server_port']), factory=factory) '''

        return factory

    except Exception as e:
        logging.exception(e)
        raise e



def getReactor():
    return reactor
