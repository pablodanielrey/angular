import copy
from model.dao import DAO

class WampTransport:

    def __init__(self):
        self.protocol = None
        self.http_headers_received = None
        self.http_headers_sent = None
        self.type = None
        self.peer = None
        self.cbtid = None

    @classmethod
    def fromDetails(cls, details):
        c = cls()
        c.__dict__ = details
        return c


class WampSession:
    transportClass = WampTransport

    def __init__(self):
        self.authid = None
        self.authrole = None
        self.authmethod = None
        self.authprovider = None
        self.transport = None
        self.session = None

    @classmethod
    def fromDetails(cls, details):
        print(details)
        d = copy.deepcopy(details)
        c = cls()
        c.__dict__ = d
        c.authid = str(c.authid)
        c.transport = cls.transportClass.fromDetails(d['transport'])
        return c

    @classmethod
    def findById(cls, con, sid):
        return WampSessionDAO.findById(con, sid)

    def create(self, con):
        WampSessionDAO.persist(con, self)

    def destroy(self, con):
        WampSessionDAO.destroy(con, self)


class WampSessionDAO(DAO):

    @classmethod
    def _fromResult(cls, r):
        t = WampTransport()
        t.protocol = r['protocol']
        t.http_headers_received = r['http_headers_received']
        t.http_headers_sent = r['http_headers_sent']
        t.type = r['type']
        t.peer = r['peer']
        t.cbtid = r['cbtid']

        s = WampSession()
        s.authid = r['auth_id']
        s.authrole = r['auth_role']
        s.authmethod = r['auth_method']
        s.authprovider = r['auth_provider']
        s.session = r['session']
        s.transport = t

        return s

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists systems;

                create table IF NOT EXISTS systems.wamp_sessions (
                    session varchar,
                    auth_id varchar,
                    auth_role varchar,
                    auth_method varchar,
                    auth_provider varchar,
                    protocol varchar,
                    http_headers_sent varchar,
                    http_headers_received varchar,
                    type varchar,
                    peer varchar,
                    cbtid varchar,
                    created timestamptz default now(),
                    deleted timestamptz
                );
            """)
        finally:
            cur.close()

    @classmethod
    def destroy(cls, con, s):
        cur = con.cursor()
        try:
            cur.execute('update systems.wamp_sessions set deleted = NOW() where session = %s', (s.session,))
            if cur.rowcount <= 0:
                raise Exception('Session not found {}'.format(s.session))
        finally:
            cur.close()

    @classmethod
    def persist(cls, con, s):
        cur = con.cursor()
        try:
            cur.execute('select session from systems.wamp_sessions where session = %s and deleted is null', (s.session,))
            if cur.rowcount >= 0:
                """ ya existe una sesión con ese id """
                return

            data = {}
            data = s.__dict__.copy()
            data.update(s.transport.__dict__.copy())
            data['http_headers_sent'] = str(data['http_headers_sent'])
            data['http_headers_received'] = str(data['http_headers_received'])
            print(data)
            cur.execute('insert into systems.wamp_sessions '
                        '(session, auth_id, auth_role, auth_method, auth_provider, protocol, http_headers_sent, http_headers_received, type, peer, cbtid) '
                        'values '
                        '(%(session)s, %(authid)s, %(authrole)s, %(authmethod)s, %(authprovider)s, %(protocol)s, %(http_headers_sent)s, %(http_headers_received)s, %(type)s, %(peer)s, %(cbtid)s)',
                        data)
        finally:
            cur.close()

    @classmethod
    def findById(cls, con, sid):
        cur = con.cursor()
        try:
            cur.execute('select * from systems.wamp_sessions where session = %s', (sid,))
            return [cls._fromResult(c) for c in cur]
        finally:
            cur.close()
