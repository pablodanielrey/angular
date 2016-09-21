
"""
from autobahn.wamp.exception import ApplicationError
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.python import log
"""

import autobahn

import copy
from model.session.wamp import WampTransport, WampSession
import wamp


class SessionLink:

    def __init__(self, realm):
        self.realm = realm

    @autobahn.wamp.subscribe('wamp.session.on_join')
    def on_session_join(self, details):
        print('join - {}'.format(self.realm))
        session = WampSession.fromDetails(details)
        conn = wamp.getConnectionManager()
        con = conn.get()
        try:
            session.create(con)
            con.commit()
        finally:
            conn.put(con)

    @autobahn.wamp.subscribe('wamp.session.on_leave')
    def on_session_leave(self, sid):
        print('leave - {}'.format(self.realm))
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


class WampSessionComponent(wamp.SystemComponentSession):
    def getWampComponents(self):
        return [SessionLink(self.config.realm)]
