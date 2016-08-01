
"""
    Autenticadores de crossbar
    Proveen un método de autentificación de los transportes de corssbar contra el modelo de los sistemas implementados en python
    Se configuran como un componente del router de crossbar.



    Los campos que puede retornar un autenticador dinámico son :

    {
        'realm': '',
        'authid': '',
        'role': '',
        'extra': {}
    }

    referencia: crossbar.router.auth.pending.PendingAuth._assign_principal

"""

import datetime
import dateutil.tz

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
import uuid
import autobahn
import inject
inject.configure_once()

import wamp


class AnonymousAuth(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):

        def authenticate(realm, authid, details):
            principal = {
                'realm': 'public',
                'role': 'anonymous',
                'extra': {
                    'message': 'anonymous auth'
                }
            }
            return principal

        yield self.register(authenticate, 'authenticate.anonymous')


class TicketAuth(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):

        from model.login.login import Login
        login = inject.instance(Login)

        @inlineCallbacks
        def authenticate(realm, authid, details):
            username = wamp.getWampCredentials()['username']
            password = wamp.getWampCredentials()['password']

            """ chequeo si es un componente del sistema """
            if authid == username and details['ticket'] == password:
                principal = {
                    'role': 'system',
                    'extra': {
                        'message': 'system component'
                    }
                }
                return principal

            """ chequeo si es un token ya generado """
            token = yield self.call('authenticate.check_user_token', authid, details['ticket'])
            print(authid)
            print(details['ticket'])
            print(token)
            if token:
                principal = {
                    'role': 'authenticated',
                    'extra': token
                }
                return principal

            """ chequeo si es un usuario de la base de datos """
            con = wamp.getConnectionManager().get()
            try:
                username = authid
                password = details['ticket']
                if not login.login(con, username, password):
                    raise ApplicationError('usuario o clave incorrectas')

                token = yield self.call('authenticate.get_new_token', username);
                principal = {
                    'role': 'authenticated',
                    'extra': token
                }
                return principal

            except ApplicationError as ae:
                raise ae
            except Exception as e:
                raise ApplicationError('exception in ticket authenticator')

            finally:
                wamp.getConnectionManager().put(con)

        yield self.register(authenticate, 'authenticate.ticket')


class TokenGeneratorComponent(wamp.SystemComponentSession):

    expiration = 60
    tokens = {}

    def _getNewExpiration(self):
        return (datetime.datetime.now(dateutil.tz.tzlocal()) + datetime.timedelta(seconds=self.expiration))

    @autobahn.wamp.register('authenticate.get_new_token')
    def getNewToken(self, username):
        token = str(uuid.uuid4())
        expire = self._getNewExpiration()
        tokenData = {
            'username': username,
            'ticket': token,
            'expires': expire.isoformat()
        }
        self.tokens[token] = {
            'username': username,
            'expires': expire
        }
        return tokenData

    @autobahn.wamp.register('authenticate.check_user_token')
    def checkUserToken(self, username, token):
        if token in self.tokens.keys():
            tk = self.tokens[token]
            print(tk)
            if (tk and tk['username'] == username):
                if (tk['expires'] > datetime.datetime.now(dateutil.tz.tzlocal())):
                    tk['expires'] = self._getNewExpiration()
                    tokenData = {
                        'username': username,
                        'ticket': token,
                        'expires': tk['expires'].isoformat()
                    }
                    return tokenData
                else:
                    print('removiendo token expirado {}'.format(token))
                    del self.tokens[token]
        return None



"""
class CRAAuth(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):

        import inject
        inject.configure_once()

        from model.connection.connection import Connection
        from model.registry import Registry
        from model.users.users import UserPassword

        reg = inject.instance(Registry)
        conn = Connection(reg.getRegistry('crossbar'))

        def authenticate(realm, authid, details):
            con = conn.get()
            try:
                identities = UserPassword.findByUsername(con, authid)
                if len(identities) <= 0 or identities[0].password is None:
                    raise ApplicationError('usuario o clave incorrectas')

                principal = {
                    'secret': identities[0].password,
                    'role': 'authenticated',
                    'extra': {
                        'message': 'cra auth'
                    }
                }
                return principal

            except Exception as e:
                raise ApplicationError(e)

            finally:
                conn.put(con)

        yield self.register(authenticate, 'login.authenticate.cra')
"""
