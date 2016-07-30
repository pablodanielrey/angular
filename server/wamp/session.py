
from autobahn.wamp.exception import ApplicationError
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.python import log

import copy
from model.serializer.ditesiSerializer import _my_loads, JSONSerializable

class Transport(JSONSerializable):

    def __init__(self):
        self.protocol = None
        self.http_headers_received = None
        self.http_headers_sent = None
        self.type = None
        self.peer = None
        self.cbtid = None


class Session(JSONSerializable):

    def __init__(self):
        self.authid = None
        self.authrole = None
        self.authmethod = None
        self.authprovider = None
        self.transport = None
        self.session = None


def addJsonSerializableFields(details):
    details['__json_class__'] = 'Session'
    details['__json_module__'] = 'wamp.session'
    if 'transport' in details:
        details['transport']['__json_class__'] = 'Transport'
        details['transport']['__json_module__'] = 'wamp.session'

def on_session_join(details):
    print('-------------------------on_join-------------------------------------')
    d = copy.deepcopy(details)

    t = Transport()
    t.__dict__ = d['transport']

    s = Session()
    s.__dict__ = d
    s.transport = t

    print(s.authid)
    print(s.transport.peer)

def on_session_leave(details):
    print(details);


class WampSession(ApplicationSession):

    def onConnect(self):
        self.join("core", ["ticket"], "system")

    def onChallenge(self, challenge):
        if challenge.method == 'ticket':
            return 'password'
        else:
            raise Exception('Invalid auth method {}'.format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):

        yield self.subscribe(on_session_join, 'wamp.session.on_join')
        yield self.subscribe(on_session_leave, 'wamp.session.on_leave')
