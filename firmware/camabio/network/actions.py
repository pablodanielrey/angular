import json, base64, datetime, traceback, logging
import inject

from twisted.internet.defer import inlineCallbacks, returnValue

from model.exceptions import *

from model.events import Events

from firmware import Firmware

class Enroll:

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


    @inlineCallbacks
    def handleAction(self, server, message):

        if (message['action'] != 'enroll'):
            return False

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        if 'dni' not in message['request']:
            response = {'id':message['id'], 'error':'Insuficientes parámetros, falta el dni'}
            server.sendMessage(response)
            return True

        dni = message['request']['dni']


        try:
            requests = yield self.firmware.enroll(dni,
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
            returnValue(True)

        except Exception as e:
            server.sendError(message,e)
            raise e
