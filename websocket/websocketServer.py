# -*- coding: utf-8 -*-
from Ws.SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import json, base64
import datetime
import traceback
import logging
from wexceptions import MalformedMessage
from model.profiles import AccessDenied
from model.utils import DateTimeEncoder



class NullData(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__


class NotImplemented(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__



class WebsocketServer(WebSocket):

  def setActions(self,actions):
    self.actions = actions

  def sendException(self,e):
      msg = {'type':'Exception','name':e.__class__.__name__}
      self.sendMessage(msg)

  def sendError(self,msg,e):
      mmsg = {'id':msg['id'],'error':e.__class__.__name__}
      self.sendMessage(mmsg)

  def handleMessage(self):
    try:
      if self.data is None:
        raise NullData()

      print('C:' + self.data)
      message = json.loads(str(self.data))

      if 'action' not in message:
        raise MalformedMessage()

      if 'id' not in message:
        raise MalformedMessage()

      try:
          managed = False
          for action in self.actions:
            managed = action.handleAction(self,message)
            if managed:
              break

      except AccessDenied as e:
          print(e.__class__.__name__ + ' ' + str(e))
          traceback.print_exc()
          self.sendError(message,e)
          managed = True

      except Exception as e:
          print(e.__class__.__name__ + ' ' + str(e))
          traceback.print_exc()
          self.sendError(message,e)
          raise e

      if not managed:
        raise NotImplemented()

    except Exception as e:
      print(e.__class__.__name__ + ' ' + str(e))
      traceback.print_exc()
      self.sendException(e)


  def chunks(self,l,n):
      n = max(1,n)
      return [l[i:i+n] for i in range(0, len(l), n)]


  def sendMessage(self,msg):
      jmsg = json.dumps(msg,cls=DateTimeEncoder)
      if (len(jmsg) < 1000):
          logging.debug(jmsg)

      super(WebsocketServer,self).sendMessage(jmsg)

      #maxMessageSize = 1000
      #if len(jmsg) > maxMessageSize:
          #""" hago framing del mensaje """
          #data = self.chunks(jmsg,maxMessageSize)

          #""" envío la cabecera """
          #msg2 = {'id': msg['id'], 'parts': len(data), 'ok':''}
          #jmsg2 = json.dumps(msg2)
          #logging.debug(jmsg2);
          #super(WebsocketServer,self).sendMessage(jmsg2)

          #""" envío los datos en mensajes separados """
          #index = 0
          #for d in data:
              #msg2 = { 'id': msg['id'], 'part_number':index, 'part_data': base64.b64encode(d), 'ok':'' }
              #jmsg2 = json.dumps(msg2)
              #logging.debug(jmsg2);
              #super(WebsocketServer,self).sendMessage(jmsg2)
              #index = index + 1

      #else:
          #logging.debug(jmsg);
          #super(WebsocketServer,self).sendMessage(jmsg)



  def handleConnected(self):
    print(("connected : ",self.address))

  def handleClose(self):
    print(("closed : ",self.address))
