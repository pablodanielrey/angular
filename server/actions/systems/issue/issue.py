# -*- coding: utf-8 -*-
import inject
import logging
import psycopg2

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config
from model.systems.issue.issue import Issue
from model.systems.issue.issueModel import IssueModel

class WampIssue(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.issueModel = inject.instance(IssueModel)
        self.issue = inject.instance(Issue)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.newIssue_async,'issue.issue.newIssue')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def newIssue(self, issue):
        con = self._getDatabase()
        try:
            self.issueModel.insert(con,issue)
            con.commit()
            return True

        finally:
            con.close()

    @coroutine
    def newIssue_async(self, issue):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.newIssue, issue)
        return r
