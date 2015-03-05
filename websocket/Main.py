# -*- coding: utf-8 -*-
import signal, sys
import inject
import thread
import time
import logging

''' para la parte web '''
import SocketServer
from httpServer import MyHttpServerRequestHandler

''' el core de websockets '''
from Ws.SimpleWebSocketServer import SimpleWebSocketServer
from Ws.SimpleWebSocketServer import SimpleSSLWebSocketServer
from websocketServer import WebsocketServer


from actions.chat import SendEventToClients
from actions.login import Login, Logout, ResetPassword, ChangePassword
from actions.requests import CreateAccountRequest, ConfirmAccountRequest, ListAccountRequests, ApproveAccountRequest, RemoveAccountRequest
from actions.users import UpdateUser, FindUser, ListUsers, ListMails, PersistMail, ConfirmMail, RemoveMail
from actions.status import GetStatus
from actions.students import CreateStudent, FindStudent, PersistStudent
from actions.groups import ListGroups, FindGroup, FindMembers, RemoveMembers, AddMembers, UpdateGroup, CreateGroup
from actions.systems import ListSystems
from actions.laboralInsertion import PersistLaboralInsertion, FindLaboralInsertion, CreateLanguages,PersistLanguage, DeleteLanguage, FindLanguage, ListLanguages, CreateDegrees, PersistDegree, DeleteDegree, FindDegree, ListDegree, AcceptTermsAndConditions, CheckTermsAndConditions
from actions.profiles import CheckAccess

from model.session import Session
from model.config import Config

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
    SendEventToClients(),
    Login(), Logout(), ResetPassword(), ChangePassword(),
    CreateAccountRequest(), ConfirmAccountRequest(), ListAccountRequests(), ApproveAccountRequest(), RemoveAccountRequest(),
    ListUsers(), UpdateUser(), FindUser(), ListMails(), PersistMail(), ConfirmMail(), RemoveMail(),
    GetStatus(),
    CreateStudent(), FindStudent(), PersistStudent(),
    ListGroups(), FindGroup(), FindMembers(), RemoveMembers(), AddMembers(), UpdateGroup(), CreateGroup(),
    ListSystems(),
    PersistLaboralInsertion(), FindLaboralInsertion(), CreateLanguages(), PersistLanguage(), DeleteLanguage(), FindLanguage(), ListLanguages(), CreateDegrees(), PersistDegree(), DeleteDegree(), FindDegree(), ListDegree(), AcceptTermsAndConditions(), CheckTermsAndConditions(),
    CheckAccess()
  ]


  ''' codigo de inicialización del servidor '''

  websocketServer = SimpleWebSocketServer(config.configs['server_ip'],int(config.configs['server_port']),WebsocketServer,actions)
  #websocketSslServer = SimpleSSLWebSocketServer(config.configs['server_ssl_ip'],int(config.configs['server_ssl_port']),WebsocketServer,actions, config.configs['server_ssl_cert'],config.configs['server_ssl_key'])
  #httpServer = SocketServer.TCPServer(('192.168.0.100',8002), MyHttpServerRequestHandler)

  def close_sig_handler(signal,frame):
    websocketServer.close()
    #websocketSslServer.close();
    #httpServer.shutdown()
    sys.exit()

  signal.signal(signal.SIGINT,close_sig_handler)

  thread.start_new_thread(serveWebsockets,(websocketServer,1))
  #thread.start_new_thread(serveWebsockets,(websocketSslServer,1))
  #thread.start_new_thread(serveHttp,(httpServer,1))

  while True:
    time.sleep(1000)
