# -*- coding: utf-8 -*-

"""
    código que realizó emanuel para comunicarse con el firmware del reloj.
    vamos a ir por otro enfoque ahora.
    zkSoftware
"""

from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.internet import reactor
import json, base64
import psycopg2
import inject
import datetime
import traceback
import logging
from model.exceptions import MalformedMessage
from model.profiles import AccessDenied
from model.utils import DateTimeEncoder
from model.config import Config
from model.users.users import Users
from model.systems.assistance.assistance import Assistance
from model.systems.assistance.logs import Logs

class AssistanceWebSocketClient():

    def handle(self,config):
        print("ws://"+config.configs['websocketClient_ip']+":"+config.configs['websocketClient_port']+"/websocket")
        #ws = create_connection("ws://"+config.configs['websocketClient_ip']+":"+config.configs['websocketClient_port']+"/websocket")
        ws = create_connection("wss://echo.websocket.org")

        print(ws)
        print("Sending 'Hello, World'...")
        ws.send("Hello, World")
        print("Sent")
        print("Reeiving...")
        result =  ws.recv()
        print("Received '%s'" % result)
        ws.close()




class AssistanceWebsocketServer(WebSocketServerProtocol):

  config = inject.attr(Config)
  logs = inject.attr(Logs)


  def onMessage(self, payload, isBinary):
    try:

        if isBinary:
            """ por ahora no manejo mensajes binarios """
            return

        logging.debug("Decode")
        msg = payload.decode('utf-8')

        """
        self.data = attLog;datos-del-log-en-json
        """

        cmdLog = "attLog;"
        if not(msg.startswith(cmdLog)):
          """ lo ignoro ya que no es un mensaje de log desde el firmware """
          return


        msgstr = msg[len(cmdLog):]

        try:
          con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

          logging.debug("JSON")
          log = self.logs.fromJsonMessage(con,msgstr)

          logging.debug("PERSIST")
          self.logs.persist(con,log)


          con.commit()
          logging.debug("COMMIT")

          """ ya tengo guardado el log, por lo que lo elimino del firmware """
          response = ("OK;delete;"+log['id']).encode('utf-8')
          self.sendMessage(response,False);

        except psycopg2.DatabaseError as e:
          logging.debug(e)
          con.rollback()
          raise e

        except Exception as e2:
          traceback.print_exc()
          logging.debug(e2)
          raise e2

        finally:
          con.close()



    except Exception as e:
      print(e.__class__.__name__ + ' ' + str(e))
      """
      traceback.print_exc()
      self.sendException(e)
      """



  def onConnect(self,cr):
        logging.debug('cliente conectado')
        logging.debug(cr)
        return None

  def onClose(self,wasClean, code, reason):
      print('cliente desconectado {0}, {1}, {2}'.format(wasClean,code,reason))
      logging.debug('cliente desconectado {0}, {1}, {2}'.format(wasClean,code,reason))

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):

    def __init__(self, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = []


    def register(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        print("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c._sendEncodedMessage(msg)
            print("message sent to {}".format(c.peer))





def getReactor():
    config = inject.instance(Config)
    # log.startLogging(sys.stdout)
    factory = BroadcastServerFactory()
    factory.protocol = AssistanceWebsocketServer
    reactor.listenTCP(8026, factory)
    return reactor
