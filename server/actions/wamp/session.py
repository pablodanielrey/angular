
from autobahn.wamp.exception import ApplicationError
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.python import log

class WampSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def on_join(details):
            print(details);

        def on_leave(details):
            print(details);

        yield self.subscribe(on_join, 'wamp.session.on_join');
        yield self.subscribe(on_leave, 'wamp.session.on_leave');
