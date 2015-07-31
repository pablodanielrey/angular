# -*- coding: utf-8 -*-
import inject

from model.profiles import Profiles
from model.config import Config
from model.exceptions import *

"""
    Modulo de acceso al manejo de perfiles/roles
"""


"""
peticion:
{
    "id":"",
    "action":"checkAccess",
    "session":"session de usuario",
    "profiles":"profile list coma separated ej: ADMIN,USER"
}

respuesta:
{
    "id":"id de la peticion",
    "response":"granted|not granted"
    "ok":"",
    "error":""
}

"""

class CheckAccess:

  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if (message['action'] != 'checkAccess'):
        return False

    if 'profiles' not in message:
        raise MalformedMessage()

    profile_list = message['profiles']
    role_list = profile_list.split(',')

    import pdb
    pdb.set_trace()
    try:
        """ chequeo tener permiso como usuario como minimo """
        sid = message['session']
        self.profiles.checkAccess(sid,role_list)

        response = {'id':message['id'], 'ok':'', 'response':'granted'}
        server.sendMessage(response)

    except AccessDenied as e:
        response = {'id':message['id'], 'ok':'', 'response':'not granted'}
        server.sendMessage(response)

    return True
