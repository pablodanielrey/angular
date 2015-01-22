# -*- coding: utf-8 -*-
import signal, sys
import inject
import thread
import time

''' para la parte web '''
import SocketServer
from httpServer import MyHttpServerRequestHandler

''' el core de websockets '''
from Ws.SimpleWebSocketServer import SimpleWebSocketServer
from websocketServer import WebsocketServer


from actions.chat import SendEventToClients
from actions.login import Login, Logout, ResetPassword, ChangePassword
from actions.requests import CreateAccountRequest, ListAccountRequests, ApproveAccountRequest, RemoveAccountRequest
from actions.users import UpdateUser, FindUser, ListUsers, ListMails, PersistMail, ConfirmMail, RemoveMail
from actions.status import GetStatus
from actions.students import CreateStudent, FindStudent
from actions.groups import ListGroups, FindGroup, FindMembers, RemoveMembers, AddMembers, UpdateGroup, CreateGroup
from actions.systems import ListSystems

from model.session import Session
from model.config import Config

def config_injector(binder):
    binder.bind(Session,Session())


def serveWebsockets(server, *args):
    server.serveforever()

def serveHttp(server, *args):
    server.serve_forever()


if __name__ == '__main__':


  inject.configure(config_injector)
  config = inject.instance(Config)

  ''' aca se definen las acciones a ser manejadas por el server de websocket '''

  actions = [
    SendEventToClients(),
    Login(), Logout(), ResetPassword(), ChangePassword(),
    CreateAccountRequest(), ListAccountRequests(), ApproveAccountRequest(), RemoveAccountRequest(),
    ListUsers(), UpdateUser(), FindUser(), ListMails(), PersistMail(), ConfirmMail(), RemoveMail(),
    GetStatus(),
    CreateStudent(), FindStudent(),
    ListGroups(), FindGroup(), FindMembers(), RemoveMembers(), AddMembers(), UpdateGroup(), CreateGroup(),
    ListSystems()
  ]


  ''' codigo de inicialización del servidor '''

  websocketServer = SimpleWebSocketServer(config.configs['server_ip'],int(config.configs['server_port']),WebsocketServer,actions)
#  httpServer = SocketServer.TCPServer(('192.168.0.100',8002), MyHttpServerRequestHandler)

  def close_sig_handler(signal,frame):
    websocketServer.close()
    #httpServer.shutdown()
    sys.exit()

  signal.signal(signal.SIGINT,close_sig_handler)

  thread.start_new_thread(serveWebsockets,(websocketServer,1))
#  thread.start_new_thread(serveHttp,(httpServer,1))

  while True:
    time.sleep(1000)
