import json, base64, datetime, traceback, logging
import inject

from model.exceptions import *

from model.events import Events

from firmware import Firmware

class Enroll:

    firmware = inject.attr(Firmware)

    def broadcast(self,server,msg,response):
        server.broadcast(
            {
                
            }
        )

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
            requests = self.firmware.enroll(dni,
                lambda: server.broadcast('primera huella'),
                lambda: server.broadcast('segunda huella'),
                lambda: server.broadcast('tercera huella'),
                lambda: server.broadcast('liberar dedo')
                )

            response = {
                'id':message['id'],
                'ok':'Ok'
            }

            server.sendMessage(response)
            return True

        except Exception as e:
            raise e
