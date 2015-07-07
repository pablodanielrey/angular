# -*- coding: utf-8 -*-
import inject, psycopg2, logging

from model.config import Config
from model.session import Session

from model.exceptions import *



class Profiles:

    session = inject.attr(Session)
    config = inject.attr(Config)


    def _checkAccessWithCon(self,con,sid,roles):

        if sid is None:
            return False

        s = self.session._getSession(con,sid)
        if s is None:
            return False

        user_id = s[self.config.configs['session_user_id']]
        if user_id == None:
            logging.debug('no se encuenta user_id con el id de sesión %s' % sid)
            return False

        """ por ahora cualquier usuario logueado exitósamente es usuario """
        if 'USER' in roles:
            return True;

        try:
            cur = con.cursor()
            cur.execute('select profile from credentials.auth_profile where user_id = %s',(user_id,))
            rdata = cur.fetchall()
            if rdata == None:
                logging.debug('el usuario con id %s no tiene ningun rol asignado' % user_id)
                return False

            for role in rdata:
                if role[0] in roles:
                  return True

            logging.debug('no se encuentan los roles asignados al usuario (%s) en la lista de roles pedidos %s' % (rdata,tuple(roles)))
            return False

        except Exception as e:
            logging.exception(e)
            return False




    """
        chequeo si el usuario identificado con la sesion = sid, tiene alguno de los roles pasados dentro de la lista roles
        en el caso de que tenga alguno retorno true.
        en caso de no tener ninguno tiro false
    """
    def _checkAccess(self,sid,roles):

        if sid is None:
            return False

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            return self.__checkAccessWithCon(con,sid,roles)

        except Exception as e:
            logging.exception(e)
            return False

        finally:
            if con:
                con.close()





    """
        chequeo si el usuario identificado con la sesion = sid, tiene alguno de los roles pasados dentro de la lista roles
        en el caso de que tenga alguno retorno true.
        en caso de no tener ninguno o error dispara AccessDenied
    """
    def checkAccess(self,sid,roles):

        if self._checkAccess(sid,roles):
            return True
        else:
            raise AccessDenied()



    def getLocalUserId(self,sid):
        s = self.session.getSession(sid)
        user_id = s[self.config.configs['session_user_id']]
        return user_id
