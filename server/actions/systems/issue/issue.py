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
from model.profiles import Profiles

class WampIssue(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.issueModel = inject.instance(IssueModel)
        self.issue = inject.instance(Issue)
        self.profiles = inject.instance(Profiles)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.newIssue_async,'issue.issue.newIssue')
        yield from self.register(self.getIssues_async, "issue.issue.getIssues")
        yield from self.register(self.deleteIssue_async, "issue.issue.deleteIssue")
        yield from self.register(self.updateIssueData_async, "issue.issue.updateIssueData")

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def newIssue(self, sessionId, issue, state, visibilities):
        con = self._getDatabase()
        try:
            userId = self.profiles.getLocalUserId(sessionId)
            id = self.issue.create(con,issue,userId,visibilities) if state is None else self.issue.create(con,issue,userId,visibilities,state)
            con.commit()
            return id
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            con.close()

    @coroutine
    def newIssue_async(self, sessionId, issue, state, visibilities):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.newIssue, sessionId, issue, state, visibilities)
        return r

    # Retorna todas las issues solicitadas por el usuario o aquellas cuyo responsable es el usuario
    # si el userId es null tomo por defecto el id del usuario logueado
    def getIssues(self, sessionId, userId):
        con = self._getDatabase()
        try:
            if userId is None:
                userId = self.profiles.getLocalUserId(sessionId)
            return self.issue.getIssues(con,userId)
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            con.close()

    @coroutine
    def getIssues_async(self, sessionId, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getIssues, sessionId, userId)
        return r


    def deleteIssue(self, id):
        con = self._getDatabase()
        try:
            self.issue.delete(con,id)
            con.commit()
            return True
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            con.close()

    @coroutine
    def deleteIssue_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.deleteIssue, id)
        return r

    #  Actualiza los datos del issue
    #  userId Id del usuario que solicita la actualizacion de datos (quiza sea alguien diferente a quien solicito el issue)
    def updateIssueData(self, sessionId, issuer, userId):
        con = self._getDatabase()
        try:
            if userId is None:
                userId = self.profiles.getLocalUserId(sessionId)
            id = self.issue.updateData(con,issuer,userId)
            con.commit()
            return id
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            con.close()

    @coroutine
    def updateIssueData_async(self, sessionId, issuer, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.updateIssueData, sessionId, issuer, userId)
        return r
