
from autobahn.wamp.exception import ApplicationError
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.python import log

import copy
from model.session.wamp import WampTransport, WampSession
import wamp


class SessionLink:

    def __init__(self, realm):
        self.realm = realm

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




class WampSessionComponent(ApplicationSession):

    def onConnect(self):
        """
            ejemplo de lectura de parámetros desde la config.json de crossbar
            self.config.extra['parametro1']
        """
        self.join(self.config.realm, ["ticket"], wamp.getWampCredentials()['username'])

    def onChallenge(self, challenge):
        if challenge.method == 'ticket':
            return wamp.getWampCredentials()['password']
        else:
            raise Exception('Invalid auth method {}'.format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):
        link = SessionLink(self.config.realm)
        yield self.subscribe(link.on_session_join, 'wamp.session.on_join')
        yield self.subscribe(link.on_session_leave, 'wamp.session.on_leave')
