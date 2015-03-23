# -*- coding: utf-8 -*-
from Ws.SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from websocket import create_connection
import json, base64
import psycopg2
import inject
import datetime
import traceback
import logging
from wexceptions import MalformedMessage
from model.profiles import AccessDenied
from model.utils import DateTimeEncoder
from model.config import Config
from model.users import Users
from model.systems.assistance.assistance import Assistance
from model.systems.assistance.logs import Logs

class AssistanceWebSocketClient():

    def handle(self,config):
        print "ws://"+config.configs['websocketClient_ip']+":"+config.configs['websocketClient_port']+"/websocket"
        #ws = create_connection("ws://"+config.configs['websocketClient_ip']+":"+config.configs['websocketClient_port']+"/websocket")
        ws = create_connection("wss://echo.websocket.org")

        print ws
        print "Sending 'Hello, World'..."
        ws.send("Hello, World")
        print "Sent"
        print "Reeiving..."
        result =  ws.recv()
        print "Received '%s'" % result
        ws.close()




class AssistanceWebsocketServer(WebSocket):

  config = inject.attr(Config)
  logs = inject.attr(Logs)

  def handleMessage(self):
    try:

      if self.data is None:
        raise NullData()

      """
      self.data = attLog;datos-del-log-en-json
      """

      cmdLog = "attLog;"
      if not(self.data.startswith(cmdLog)):
          """ lo ignoro ya que no es un mensaje de log desde el firmware """
          return

      msgstr = self.data[len(cmdLog):]

      try:
          con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

          log = self.logs.fromJsonMessage(msgstr)
          self.logs.persist(con,log)

          con.commit()

          """ ya tengo guardado el log, por lo que lo elimino del firmware """
          super(AssistanceWebsocketServer,self).sendMessage("OK;delete;"+str(log_id));

      except psycopg2.DatabaseError, e:
          con.rollback()
          raise e

      finally:
          con.close()



    except Exception as e:
      print e.__class__.__name__ + ' ' + str(e)
      """
      traceback.print_exc()
      self.sendException(e)
      """



  def handleConnected(self):
    print("connected : ",self.address)

  def handleClose(self):
    print("closed : ",self.address)
