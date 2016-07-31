
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
import autobahn

import wamp
from model.serializer.ditesiSerializer import JSONSerializable

#from model.serializer import ditesiSerializer
#ditesiSerializer.register()


class LoginPublicSession(ApplicationSession):

    @autobahn.wamp.register('login.get_basic_data')
    def getBasicData(self, dni):
        print('-getBasicData')
        return {
            'name':'n',
            'lastname':'p',
            'photo':'dd'
        }

    def onConnect(self):
        username = wamp.getWampCredentials()['username']
        self.join("public", ["ticket"], username)

    def onChallenge(self, challenge):
        if challenge.method == 'ticket':
            return wamp.getWampCredentials()['password']
        else:
            raise Exception('Invalid auth method {}'.format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):
        results = yield self.register(self)
        for res in results:
            if isinstance(res, autobahn.wamp.protocol.Registration):
                print("Ok, registered procedure with registration ID {}".format(res.id))
            else:
                print("Failed to register procedure: {}".format(res))


class LoginSession(ApplicationSession):

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
        results = yield self.register(self)
        for res in results:
            if isinstance(res, autobahn.wamp.protocol.Registration):
                print("Ok, registered procedure with registration ID {}".format(res.id))
            else:
                print("Failed to register procedure: {}".format(res))
