# -*- coding: utf-8 -*-

import inject, logging, json
import asyncio
import websockets

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

from model.config import Config
from model.utils import DateTimeEncoder


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
  yield from websocket.send(jmsg)












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


def getServer():
    logger = logging.getLogger('websockets.server')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    config = inject.instance(Config)
    return websockets.server.serve(actionsServer,host=config.configs['server_ip'],port=int(config.configs['server_port']))
