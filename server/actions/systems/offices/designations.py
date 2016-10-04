# -*- coding: utf-8 -*-
from model.offices.designation import Designation
import wamp
import autobahn
from twisted.internet.defer import inlineCallbacks
import logging
logging.getLogger().setLevel(logging.INFO)


class Designations(wamp.SystemComponentSession):

    conn = wamp.getConnectionManager()

    @autobahn.wamp.register('offices.find_all_by_office')
    def findOfficesByUser(self, oid):
        con = self.conn.get()
        try:
            return Designation.findAllByOffice(con, oid)
        finally:
            self.conn.put(con)
