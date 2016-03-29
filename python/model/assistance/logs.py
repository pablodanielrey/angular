# -*- coding: utf-8 -*-

from model.serializer.utils import JSONSerializable

class Log(JSONSerializable):

    def __init__(self):
        self.id = None
        self.deviceId = None
        self.userId = None
        self.verifyMode = 0
        self.log = None
        self.created = None

    def between(self, start, end):
        return (self.log >= start and self.log <= end)


class LogDAO:

    @staticmethod
    def _fromResult(r):
        l = Log()
        l.id = r['id']
        l.deviceId = r['device_id']
        l.userId = r['user_id']
        l.verifyMode = r['verifymode']
        l.log = r['log']
        l.created = r['created']
        return l

    @staticmethod
    def findByUserId(con, ids, start, end):
        assert isinstance(ids, list)
        cur = con.cursor()
        try:
            cur.execute('select * from assistance.attlog where user_id in %s and log >= %s and log <= %s', (tuple(ids), start, end))
            return [ LogDAO._fromResult(r) for r in cur ]

        finally:
            cur.close()
