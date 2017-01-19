# -*- coding: utf-8 -*-
import inject
import json
import re
import logging
import psycopg2

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import threads

import autobahn
import wamp

from model.sileg.silegModel import SilegModel

class Sileg(wamp.SystemComponentSession):

    @autobahn.wamp.register('sileg.get_users')
    @inlineCallbacks
    def getUsers(self):
        r = yield threads.deferToThread(self._getUsers)
        returnValue(r)

    def _getUsers(self):
        try:
            ctx = wamp.getContextManager()
            ctx.getConn()
            #ctx.con.readOnly(ctx.con)
            return SilegModel.getUsers(ctx)

        finally:
            ctx.closeConn()



    @autobahn.wamp.register('sileg.get_cathedras')
    @inlineCallbacks
    def getCathedras(self):
        r = yield threads.deferToThread(self._getCathedras)
        returnValue(r)

    def _getCathedras(self):
        try:
            ctx = wamp.getContextManager()
            ctx.getConn()
            #ctx.con.readOnly(ctx.con)
            return SilegModel.getCathedras(ctx)

        finally:
            ctx.closeConn()



    @autobahn.wamp.register('sileg.find_positions_active_by_user')
    @inlineCallbacks
    def findPositionsActiveByUser(self, userId):
        r = yield threads.deferToThread(self._findPositionsActiveByUser, userId)
        returnValue(r)

    def _findPositionsActiveByUser(self, userId):
        try:
            ctx = wamp.getContextManager()
            ctx.getConn()
            #ctx.con.readOnly(ctx.con)
            return SilegModel.findPositionsActiveByUser(ctx, userId)

        finally:
            ctx.closeConn()



    @autobahn.wamp.register('sileg.find_positions_active_by_place')
    @inlineCallbacks
    def findPositionsActiveByPlace(self, placeId):
        r = yield threads.deferToThread(self._findPositionsActiveByPlace, placeId)
        returnValue(r)

    def _findPositionsActiveByPlace(self, placeId):
        try:
            ctx = wamp.getContextManager()
            ctx.getConn()
            #ctx.con.readOnly(ctx.con)
            return SilegModel.findPositionsActiveByPlace(ctx, placeId)

        finally:
            ctx.closeConn()
