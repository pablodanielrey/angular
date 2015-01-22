# -*- coding: utf-8 -*-
import inject
from model.config import Config
from model.session import Session

class AccessDenied(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__




class Profiles:

    session = inject.attr(Session)
    config = inject.attr(Config)


    def checkAccess(self,sid,roles):
        s = self.session.getSession(sid)
        user_id = s[self.config.configs['session_user_id']]

        ''' chequeo que ese usuario tenga el rol pasado por parámetro (ahora agrego el rol pasado por parametro asi siempre da ok.) '''
        current_roles = roles

        for r in current_roles:
            if r in roles:
                return True

        raise AccessDenied()


    def getLocalUserId(self,sid):
        s = self.session.getSession(sid)
        user_id = s[self.config.configs['session_user_id']]
        return user_id
