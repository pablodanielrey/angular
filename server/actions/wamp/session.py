
from autobahn.wamp.exception import ApplicationError
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.python import log

import copy
from model.seralizer.ditesiSerializer import _my_loads, JSONSerializable

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



class WampSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def addJsonSerializableFields(details):
            details['__json_class__'] = 'Session'
            details['__json_module__'] = 'wamp.session'
            if 'transport' in details:
                details['transport']['__json_class__'] = 'Transport'
                details['transport']['__json_module__'] = 'wamp.session'

        def on_join(details):
            print('-------------------------on_join-------------------------------------')
            d = copy.deepcopy(details)
            print(d);
            addJsonSerializableFields(d)
            s = _my_loads(d)

        def on_leave(details):
            print(details);

        self.log.info('registrando meta eventos')
        yield self.subscribe(on_join, 'wamp.session.on_join');
        yield self.subscribe(on_leave, 'wamp.session.on_leave');
