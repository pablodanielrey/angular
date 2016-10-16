import wamp
import autobahn

from wamp import SystemComponentSession
from model.serializer import JSONSerializable
from model.login.login import Login

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import threads


class LoginPublicSession(SystemComponentSession):

    conn = wamp.getConnectionManager()

    @autobahn.wamp.register('login.get_public_data')
    def getPublicData(self, dni):
        con = self.conn.get()
        self.conn.readOnly(con)
        try:
            return Login.getPublicData(con, dni)
        finally:
            self.conn.put(con)

class LoginSession(SystemComponentSession):

    def getRegisterOptions(self):
        return autobahn.wamp.RegisterOptions(details_arg='details')

    @autobahn.wamp.register('login.get_registered_systems')
    def getRegisteredSystems(self, details=None):
        systems = {
            'registered': [
                {
                    'domain': 'localhost',
                    'relative': '/systems/library/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'issues',
                    'relative': '/systems/issues/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'issues.econo.unlp.edu.ar',
                    'relative': '/systems/issues/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'www.issues.econo.unlp.edu.ar',
                    'relative': '/systems/issues/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'pedidos',
                    'relative': '/systems/issues/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'pedidos.econo.unlp.edu.ar',
                    'relative': '/systems/issues/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'www.pedidos.econo.unlp.edu.ar',
                    'relative': '/systems/issues/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'asistencia',
                    'relative': '/systems/assistance/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'oficinas',
                    'relative': '/systems/offices/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'oficinas.econo.unlp.edu.ar',
                    'relative': '/systems/offices/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'www.oficinas.econo.unlp.edu.ar',
                    'relative': '/systems/offices/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'assistance',
                    'relative': '/systems/assistance/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'asistencia',
                    'relative': '/systems/assistance/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'asistencia.econo.unlp.edu.ar',
                    'relative': '/systems/assistance/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': 'www.asistencia.econo.unlp.edu.ar',
                    'relative': '/systems/assistance/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                }
            ],
            'default': '/systems/login/'
        }
        return systems
