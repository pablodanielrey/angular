import json, base64, datetime, traceback, logging
import inject

from model.exceptions import *

from model.config import Config
from model.events import Events

from firmware import Firmware

class Enroll:

    config = inject.attr(Config)
    firmware = inject.attr(Firmware)

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
            requests = self.firmware.enroll(dni)

            response = {
                'id':message['id'],
                'ok':'Ok'
            }

            server.sendMessage(response)
            return True

        except Exception as e:
            raise e
