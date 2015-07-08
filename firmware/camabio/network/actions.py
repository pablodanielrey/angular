import json, base64, datetime, traceback, logging
import inject

from twisted.internet.defer import inlineCallbacks, returnValue

from model.exceptions import *

from model.events import Events
from model.profiles import Profiles
from model.credentials.credentials import UserPassword

from firmware import Firmware


class Login:

    firmware = inject.attr(Firmware)

    def _identified(self,server,log=None,user=None,sid=None,roles=None):
        msg = None
        if log:
            msg = {
                'type':'IdentifiedEvent',
                'data':{
                    'log':log,
                    'user':user,
                    'sid':sid
                }
            }
            if roles:
                msg['data']['profile'] = 'admin'

        else:
            msg = {
                'type':'IdentifiedEvent',
                'data':{
                    'msg':'Credenciales Incorrectas'
                }
            }

        server.broadcast(msg)



    def handleAction(self, server, message):

        if (message['action'] != 'login'):
            return False

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        if 'dni' not in message['request']:
            response = {'id':message['id'], 'error':'Insuficientes parámetros, falta el dni'}
            server.sendMessage(response)
            return True

        if 'password' not in message['request']:
            response = {'id':message['id'], 'error':'Insuficientes parámetros, falta la clave'}
            server.sendMessage(response)
            return True

        dni = message['request']['dni']
        password = message['request']['password']

        try:
            self.firmware.login(dni,password,self,server)

            response = {
                'id':message['id'],
                'ok':'OK'
            }
            server.sendMessage(response)
            return True

        except Exception as e:
            server.sendError(message,e)
            return True





class Enroll:

    profiles = inject.attr(Profiles)
    firmware = inject.attr(Firmware)

    def requestFinger(self,server,number):
        server.broadcast(
            {
                'type':'FingerRequestedEvent',
                'data':{
                    'fingerNumber':number
                }
            }
        )


    def sendError(self,server,error):
        server.broadcast(
            {
                'type':'ErrorEvent',
                'data':{
                    'error':error
                }
            }
        )

    def sendMsg(self,server,msg):
        server.broadcast(
            {
                'type':'MsgEvent',
                'data':{
                    'msg':msg
                }
            }
        )


    def handleAction(self, server, message):

        if (message['action'] != 'enroll'):
            return False

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        if 'sid' not in message:
            response = {'id':message['id'], 'error':'No se ha iniciado la sesión'}
            server.sendMessage(response)
            return True

        if 'dni' not in message['request']:
            response = {'id':message['id'], 'error':'Insuficientes parámetros, falta el dni'}
            server.sendMessage(response)
            return True


        ''' chequeo el nivel de acceso que tiene la persona '''
        sid = message['sid']
        if not self.profiles._checkAccess(sid,['ADMIN-ASSISTANCE']):
            response = {'id':message['id'], 'error':'Insuficiente nivel de acceso'}
            server.sendMessage(response)
            return True

        ''' userId = self.profiles.getLocalUserId(sid) '''


        dni = message['request']['dni']

        try:
            requests = self.firmware.enroll(dni,
                lambda: self.requestFinger(server,1),
                lambda: self.requestFinger(server,2),
                lambda: self.requestFinger(server,3),
                lambda: self.sendMsg(server,'Levante el dedo')
            )

            response = {
                'id':message['id'],
                'ok':'Ok'
            }

            server.sendMessage(response)
            return True

        except Exception as e:
            server.sendError(message,e)
            return True
