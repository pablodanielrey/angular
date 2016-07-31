
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

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


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

        import inject
        from model.login.login import Login
        import wamp

        inject.configure_once()
        login = inject.instance(Login)

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

            con = wamp.getConnectionManager().get()
            try:
                username = authid
                password = details['ticket']
                if not login.login(con, username, password):
                    raise ApplicationError('usuario o clave incorrectas')

                principal = {
                    'role': 'authenticated',
                    'extra': {
                        'message': 'ticket auth'
                    }
                }
                return principal

            except ApplicationError as ae:
                raise ae
            except Exception as e:
                raise ApplicationError('exception in ticket authenticator')

            finally:
                wamp.getConnectionManager().put(con)

        yield self.register(authenticate, 'authenticate.ticket')

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
