# -*- coding: utf-8 -*-
import signal, sys, json, traceback
import inject
import _thread
import time
import logging

''' para la parte web '''
import socketserver
from httpServer import MyHttpServerRequestHandler

''' el core de websockets '''
#from Ws.SimpleWebSocketServer import SimpleWebSocketServer
#from Ws.SimpleWebSocketServer import SimpleSSLWebSocketServer
#from websocketServer import WebsocketServer

#from model.assistance import AssistanceWebsocketServer

import asyncio, websockets

from actions.chat import SendEventToClients
from actions.login import Login, Logout, ResetPassword, ChangePassword
from actions.requests import CreateAccountRequest, ConfirmAccountRequest, ListAccountRequests, ApproveAccountRequest, RemoveAccountRequest, RejectAccountRequest
from actions.users import UpdateUser, FindUser, ListUsers, ListMails, PersistMail, ConfirmMail, RemoveMail
from actions.status import GetStatus
from actions.students import CreateStudent, FindStudent, PersistStudent, FindAllStudents
from actions.groups import ListGroups, FindGroup, FindMembers, RemoveMembers, AddMembers, UpdateGroup, CreateGroup
from actions.systems import ListSystems
from actions.laboralInsertion import PersistLaboralInsertion, FindLaboralInsertion, CreateLanguages,PersistLanguage, DeleteLanguage, FindLanguage, ListLanguages, CreateDegrees, PersistDegree, DeleteDegree, FindDegree, ListDegree, AcceptTermsAndConditions, CheckTermsAndConditions
from actions.profiles import CheckAccess
from actions.tutors import PersistTutorData, ListTutorData
from actions.domain import PersistDomain, DeleteDomain, FindDomain
from actions.institutionalMail import PersistInstitutionalMail, DeleteInstitutionalMail, FindInstitutionalMail

from actions.assistance.logs import GetAssistanceLogs


from model.session import Session
from model.config import Config


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










def config_injector(binder):
    binder.bind(Session,Session())


def serveWebsockets(server, *args):
    server.serveforever()

def serveHttp(server, *args):
    server.serve_forever()





if __name__ == '__main__':

  logging.basicConfig(level=logging.DEBUG);

  inject.configure(config_injector)
  config = inject.instance(Config)

  ''' aca se definen las acciones a ser manejadas por el server de websocket '''

  actions = [
#    SendEventToClients(),
#    Login(), Logout(), ResetPassword(), ChangePassword(),
#    CreateAccountRequest(), ConfirmAccountRequest(), ListAccountRequests(), ApproveAccountRequest(), RemoveAccountRequest(), RejectAccountRequest(),
#    ListUsers(), UpdateUser(), FindUser(), ListMails(), PersistMail(), ConfirmMail(), RemoveMail(),
#    GetStatus(),
#    CreateStudent(), FindStudent(), PersistStudent(), FindAllStudents(),
#    ListGroups(), FindGroup(), FindMembers(), RemoveMembers(), AddMembers(), UpdateGroup(), CreateGroup(),
#    ListSystems(),
#    PersistLaboralInsertion(), FindLaboralInsertion(), CreateLanguages(), PersistLanguage(), DeleteLanguage(), FindLanguage(), ListLanguages(), CreateDegrees(), PersistDegree(), DeleteDegree(), FindDegree(), ListDegree(), AcceptTermsAndConditions(), CheckTermsAndConditions(),
#    PersistTutorData(), ListTutorData(),
#    PersistInstitutionalMail(), DeleteInstitutionalMail(), FindInstitutionalMail(),
#    PersistDomain(), DeleteDomain(), FindDomain(),
#    CheckAccess(),
    GetAssistanceLogs()
  ]


  ''' codigo de inicialización del servidor '''

  def sendException(websocket,e):
      msg = {'type':'Exception','name':e.__class__.__name__}
      sendMessage(websocket,msg)

  def sendError(websocket,msg,e):
      mmsg = {'id':msg['id'],'error':e.__class__.__name__}
      sendMessage(websocket,mmsg)

  def sendMessage(websocket,msg):
      jmsg = json.dumps(msg,cls=DateTimeEncoder)
      if (len(jmsg) < 1000):
          logging.debug(jmsg)
      websocket.send(jmsg)


  class ServerToResponse:

      def __init__(self,websocket):
          self.websocket = websocket

      def sendMessage(self,msg):

          logging.debug('enviando mensaje')
          logging.debug(msg)

          sendMessage(self.websocket,msg)


  @asyncio.coroutine
  def manageMessage(websocket,msg):
      print('C:' + msg)
      message = json.loads(msg)

      if 'action' not in message:
        raise MalformedMessage()

      if 'id' not in message:
        raise MalformedMessage()

      try:
          managed = False
          for action in actions:
            managed = action.handleAction(ServerToResponse(websocket),message)
            if managed:
              break

      except AccessDenied as e:
          print(e.__class__.__name__ + ' ' + str(e))
          traceback.print_exc()
          sendError(websocket,message,e)
          managed = True

      except Exception as e:
          print(e.__class__.__name__ + ' ' + str(e))
          traceback.print_exc()
          sendError(websocket,message,e)
          raise e



  @asyncio.coroutine
  def actionsServer(websocket,path):
      while True:
          message = yield from websocket.recv()
          if message is None:
              break
          yield from manageMessage(websocket,message)


  #websocketServer = SimpleWebSocketServer(config.configs['server_ip'],int(config.configs['server_port']),WebsocketServer,actions)

  #websocketServerAssistance = SimpleWebSocketServer(config.configs['server_ip'],8026,AssistanceWebsocketServer,None)
  #websocketClientAssistance = AssistanceWebSocketClient()
  #websocketClientAssistance.handle(config)

  #websocketSslServer = SimpleSSLWebSocketServer(config.configs['server_ssl_ip'],int(config.configs['server_ssl_port']),WebsocketServer,actions, config.configs['server_ssl_cert'],config.configs['server_ssl_key'])
  #httpServer = SocketServer.TCPServer(('192.168.0.100',8002), MyHttpServerRequestHandler)

  def close_sig_handler(signal,frame):
    #websocketServer.close()
    #websocketSslServer.close();
    #httpServer.shutdown()
    sys.exit()

  signal.signal(signal.SIGINT,close_sig_handler)

  #_thread.start_new_thread(serveWebsockets,(websocketServer,1))
  start_server = websockets.serve(actionsServer,config.configs['server_ip'],int(config.configs['server_port']))
  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()

  #thread.start_new_thread(serveWebsockets,(websocketServerAssistance,1))
  #thread.start_new_thread(serveWebsockets,(websocketSslServer,1))
  #thread.start_new_thread(serveHttp,(httpServer,1))

  while True:
    time.sleep(1000)
