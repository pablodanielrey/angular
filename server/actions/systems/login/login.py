
import autobahn

from wamp import SystemComponentSession
from model.serializer.ditesiSerializer import JSONSerializable

#from model.serializer import ditesiSerializer
#ditesiSerializer.register()


class LoginPublicSession(SystemComponentSession):

    @autobahn.wamp.register('login.get_basic_data')
    def getBasicData(self, dni):
        print('-getBasicData')
        return {
            'name':'Nombre',
            'lastname':'Apellido',
            'photo':'data:image/jpeg;base64,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'
        }


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
                    'domain': '127.0.0.1',
                    'relative': '/systems/library/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                },
                {
                    'domain': '',
                    'relative': '/systems/login/',
                    'ticket': 'fnfwfewfewfmewfklemflfdlskmfsd'
                }
            ],
            'default': '/systems/login/'
        }
        return systems
