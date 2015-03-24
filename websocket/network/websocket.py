import inject, logging, json, sys, traceback

"""
from actions.chat import SendEventToClients
from actions.requests import CreateAccountRequest, ConfirmAccountRequest, ListAccountRequests, ApproveAccountRequest, RemoveAccountRequest, RejectAccountRequest
from actions.users import UpdateUser, FindUser, ListUsers, ListMails, PersistMail, ConfirmMail, RemoveMail
from actions.status import GetStatus
from actions.students import CreateStudent, FindStudent, PersistStudent, FindAllStudents
from actions.groups import ListGroups, FindGroup, FindMembers, RemoveMembers, AddMembers, UpdateGroup, CreateGroup
from actions.systems import ListSystems
from actions.laboralInsertion import PersistLaboralInsertion, FindLaboralInsertion, CreateLanguages,PersistLanguage, DeleteLanguage, FindLanguage, ListLanguages, CreateDegrees, PersistDegree, DeleteDegree, FindDegree, ListDegree, AcceptTermsAndConditions, CheckTermsAndConditions

from actions.tutors import PersistTutorData, ListTutorData

"""

from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor

from model.config import Config
from model.utils import DateTimeEncoder

from wexceptions import *


""" actions del core """

from actions.login.login import Login, Logout
from actions.login.password import ChangePassword, ResetPassword
from actions.profiles.profiles import CheckAccess

""" sistemas """

from actions.systems.assistance.logs import GetAssistanceLogs

from actions.systems.ntdomain.domain import PersistDomain, DeleteDomain, FindDomain
from actions.systems.mail.mail import PersistInstitutionalMail, DeleteInstitutionalMail, FindInstitutionalMail






''' aca se definen las acciones a ser manejadas por el server de websocket '''

actions = [
#    SendEventToClients(),
#    CreateAccountRequest(), ConfirmAccountRequest(), ListAccountRequests(), ApproveAccountRequest(), RemoveAccountRequest(), RejectAccountRequest(),
#    ListUsers(), UpdateUser(), FindUser(), ListMails(), PersistMail(), ConfirmMail(), RemoveMail(),
#    GetStatus(),
#    CreateStudent(), FindStudent(), PersistStudent(), FindAllStudents(),
#    ListGroups(), FindGroup(), FindMembers(), RemoveMembers(), AddMembers(), UpdateGroup(), CreateGroup(),
#    ListSystems(),
#    PersistLaboralInsertion(), FindLaboralInsertion(), CreateLanguages(), PersistLanguage(), DeleteLanguage(), FindLanguage(), ListLanguages(), CreateDegrees(), PersistDegree(), DeleteDegree(), FindDegree(), ListDegree(), AcceptTermsAndConditions(), CheckTermsAndConditions(),
#    PersistTutorData(), ListTutorData(),
    CheckAccess(),
    Login(), Logout(), ChangePassword(), ResetPassword(),
    PersistDomain(), DeleteDomain(), FindDomain(),
    PersistInstitutionalMail(), DeleteInstitutionalMail(), FindInstitutionalMail(),
    GetAssistanceLogs()
]




class ActionsServerProtocol(WebSocketServerProtocol):


    def _encodeMessage(self,msg):
        jmsg = json.dumps(msg, ensure_ascii = False, cls=DateTimeEncoder)
        if (len(jmsg) < 1000):
            logging.debug(jmsg)

        ejmsg = jmsg.encode('utf-8')
        return ejmsg

    def _sendEncodedMessage(self,msg):
        super(WebSocketServerProtocol,self).sendMessage(msg,False)



    def sendException(self,e):
        msg = {'type':'Exception','name':e.__class__.__name__}
        self.sendMessage(msg)

    def sendError(self,msg,e):
        mmsg = {'id':msg['id'],'error':e.__class__.__name__}
        self.sendMessage(mmsg)

    def sendMessage(self,msg):
        ejmsg = self._encodeMessage(msg)
        self._sendEncodedMessage(ejmsg)

    def broadcast(self,msg):
        msg = self._encodeMessage(msg)
        self.factory.broadcast(msg)



    """

            este codigo implementa el framming de los mensajes en esta capa. pero aparentemente no se necesita mas
            usando autobahn. lo dejo comentado por ahora para tenerlo a mano.

          #maxMessageSize = 1000
          #if len(jmsg) > maxMessageSize:
              #data = self.chunks(jmsg,maxMessageSize)

              #msg2 = {'id': msg['id'], 'parts': len(data), 'ok':''}
              #jmsg2 = json.dumps(msg2)
              #logging.debug(jmsg2);
              #super(WebsocketServer,self).sendMessage(jmsg2)

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

    """



    def onMessage(self, payload, isBinary):

        try:
            if isBinary:
                """ por ahora no manejo mensajes binarios """
                return

            msg = payload.decode('utf-8')
            print('C:' + msg)
            message = json.loads(msg)

            if 'action' not in message:
                raise MalformedMessage()

            if 'id' not in message:
                raise MalformedMessage()

            try:
                managed = False
                for action in actions:
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


    """ cliente se conecta. -- parametro : autobahn.websocket.protocol.ConnectionRequest """
    def onConnect(self,cr):
        logging.debug('cliente conectado')
        logging.debug(cr)
        return None

    def onOpen(self):
        logging.debug('conexión establecida')
        self.factory.register(self)

    def onClose(self,wasClean, code, reason):
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
    log.startLogging(sys.stdout)
    factory = BroadcastServerFactory()
    factory.protocol = ActionsServerProtocol
    reactor.listenTCP(int(config.configs['server_port']), factory)
    return reactor
