
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn import wamp

from model.serializer.ditesiSerializer import JSONSerializable
#from model.serializer import ditesiSerializer
#ditesiSerializer.register()

class TestSer(JSONSerializable):

    def __init__(self):
        self.rr = 'test'
        self.dd = 'test2'


class LibraryClient(ApplicationSession):

    def onConnect(self):
        self.join("core", ["ticket"], "client")

    def onChallenge(self, challenge):
        if challenge.method == 'ticket':
            return 'password'
        else:
            raise Exception('Invalid auth method {}'.format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):
        t = TestSer()
        res = yield self.call('test_serializer', t)
        print(res)
        print(res.__dict__)
