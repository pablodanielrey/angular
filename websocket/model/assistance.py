# -*- coding: utf-8 -*-
from Ws.SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import json, base64
import datetime
import traceback
import logging
from wexceptions import MalformedMessage
from model.profiles import AccessDenied
from model.utils import DateTimeEncoder


class AssistanceWebsocketServer(WebSocket):


  def handleMessage(self):
    try:
      if self.data is None:
        raise NullData()

      print 'C:' + self.data
      message = json.loads(str(self.data))

      """ decodifico el log """

      jmsg = json.dumps(msg,cls=DateTimeEncoder)

      logging.debug("lalalalaaaaaaaaaaa");

      super(WebsocketServer,self).sendMessage("{OK;}");

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
