# -*- coding: utf-8 -*-
import inject
import psycopg2
import logging
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

    """
        chequeo si el usuario identificado con la sesion = sid, tiene alguno de los roles pasados dentro de la lista roles
        en el caso de que tenga alguno retorno true.
        en caso de no tener ninguno o error dispara AccessDenied
    """
    def checkAccess(self,sid,roles):
        s = self.session.getSession(sid)
        user_id = s[self.config.configs['session_user_id']]
        if user_id == None:
            logging.debug('no se encuenta user_id con el id de sesión %s' % sid)
            raise AccessDenied()

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
          cur = con.cursor()
          cur.execute('select profile from credentials.auth_profile where user_id = %s',(user_id,))
          rdata = cur.fetchall()
          if rdata == None:
              logging.debug('el usuario con id %s no tiene ningun rol asignado' % user_id)
              raise AccessDenied()

          for role in rdata:
              if role[0] in roles:
                  return True

          logging.debug('no se encuentan los roles asignados al usuario (%s) en la lista de roles pedidos %s' % (rdata,tuple(roles)))
          raise AccessDenied()

        except psycopg2.DatabaseError, e:
            logging.exception(e)
            raise AccessDenied()

        finally:
            if con:
                con.close()




    def getLocalUserId(self,sid):
        s = self.session.getSession(sid)
        user_id = s[self.config.configs['session_user_id']]
        return user_id
