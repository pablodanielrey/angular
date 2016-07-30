
from autobahn.wamp.exception import ApplicationError
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.python import log

import copy
from model.session.wamp import WampTransport, WampSession
import wamp


class SessionLink:

    def on_session_join(self, details):
        session = WampSession.fromDetails(details)
        conn = wamp.getConnectionManager()
        con = conn.get()
        try:
            session.create(con)
            con.commit()
        finally:
            conn.put(con)

    def on_session_leave(self, sid):
        sid = str(sid)
        conn = wamp.getConnectionManager()
        con = conn.get()
        try:
            sessions = WampSession.findById(con, sid)
            for s in sessions:
                s.destroy(con)
            con.commit()
        finally:
            conn.put(con)




class WampSessionComponent(ApplicationSession):

    def onConnect(self):
        self.join("core", ["ticket"], wamp.getWampCredentials()['username'])

    def onChallenge(self, challenge):
        if challenge.method == 'ticket':
            return wamp.getWampCredentials()['password']
        else:
            raise Exception('Invalid auth method {}'.format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):
        link = SessionLink()
        yield self.subscribe(link.on_session_join, 'wamp.session.on_join')
        yield self.subscribe(link.on_session_leave, 'wamp.session.on_leave')
