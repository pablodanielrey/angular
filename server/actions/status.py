
import json
import inject

from model.exceptions import *

from model.profiles import Profiles
from model.session import Session
from model.config import Config

class GetStatus:

    profiles = inject.attr(Profiles)
    session = inject.attr(Session)

    def handleAction(self, server, message):

        if 'action' not in message:
            raise MalformedMessage()

        if message['action'] != 'getStatus':
          return False

        if 'id' not in message:
            raise MalformedMessage()

        if 'session' not in message:
            raise MalformedMessage()

        """ chequeo que exista la sesion, etc """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN'])

        msg = {
            'id': message['id'],
            'ok': '',
            'sessions': self.session.getSessions()
        }
        server.sendMessage(msg)


        return True
