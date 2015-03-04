# -*- coding: utf-8 -*-
import json, uuid, psycopg2, re
import inject
import hashlib


from model.mail import Mail
from model.users import Users
from model.events import Events
from model.profiles import Profiles
from model.config import Config
from wexceptions import MalformedMessage, AccessDenied

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

    try:
        """ chequeo tener permiso como usuario como minimo """
        sid = message['session']
        self.profiles.checkAccess(sid,role_list)

        response = {'id':message['id'], 'ok':'', 'response':'granted'}
        server.sendMessage(response)

    except AccessDenied, e:
        response = {'id':message['id'], 'ok':'', 'response':'not granted'}
        server.sendMessage(response)

    return True
