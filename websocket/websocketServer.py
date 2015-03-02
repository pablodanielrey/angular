
from Ws.SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import json
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

      print 'C:' + self.data
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
          print e.__class__.__name__ + ' ' + str(e)
          traceback.print_exc()
          self.sendError(message,e)
          managed = True

      except Exception as e:
          print e.__class__.__name__ + ' ' + str(e)
          traceback.print_exc()
          self.sendError(message,e)
          raise e

      if not managed:
        raise NotImplemented()

    except Exception as e:
      print e.__class__.__name__ + ' ' + str(e)
      traceback.print_exc()
      self.sendException(e)


  def sendMessage(self,msg):
      jmsg = json.dumps(msg,cls=DateTimeEncoder)
      logging.debug(jmsg);
      super(WebsocketServer,self).sendMessage(jmsg)


  def handleConnected(self):
    print("connected : ",self.address)

  def handleClose(self):
    print("closed : ",self.address)
