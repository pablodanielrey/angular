
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
import autobahn

import wamp
from model.serializer import JSONSerializable

#from model.serializer import ditesiSerializer
#ditesiSerializer.register()

class LibrarySession(ApplicationSession):

    @autobahn.wamp.register('test_serializer')
    def test_serializer(self, o):
        print('test_serializer llamado')
        print(o)
        if isinstance(o, JSONSerializable):
            print(o.__dict__)
        return o

    def onConnect(self):
        username = wamp.getWampCredentials()['username']
        self.join("core", ["ticket"], username)

    def onChallenge(self, challenge):
        if challenge.method == 'ticket':
            return wamp.getWampCredentials()['password']
        else:
            raise Exception('Invalid auth method {}'.format(challenge.method))


    @inlineCallbacks
    def onJoin(self, details):
        print(details)
        results = yield self.register(self)
        for res in results:
            if isinstance(res, autobahn.wamp.protocol.Registration):
                print("Ok, registered procedure with registration ID {}".format(res.id))
            else:
                print("Failed to register procedure: {}".format(res))
