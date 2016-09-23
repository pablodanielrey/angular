import wamp
import autobahn

from wamp import SystemComponentSession
from model.serializer import JSONSerializable
from model.login.login import Login

#from model.serializer import ditesiSerializer
#ditesiSerializer.register()


class LoginPublicSession(SystemComponentSession):

    conn = wamp.getConnectionManager()

    @autobahn.wamp.register('login.get_public_data')
    def getPublicData(self, dni):
        con = self.conn.get()
        try:
            return Login.getPublicData(con, dni)
        finally:
            self.conn.put(con)

class LoginSession(SystemComponentSession):

    def getRegisterOptions(self):
        return autobahn.wamp.RegisterOptions(details_arg='details')

    @autobahn.wamp.register('login.get_registered_systems')
    def getRegisteredSystems(self, details=None):
        print(details)
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
                }
            ],
            'default': '/systems/login/'
        }
        return systems
