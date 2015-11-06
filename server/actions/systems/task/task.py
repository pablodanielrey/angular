# -*- coding: utf-8 -*-
import inject
import logging
import psycopg2

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config
from model.systems.task.task import Task
from model.profiles import Profiles

class WampTask(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.task = inject.instance(Task)
        self.profiles = inject.instance(Profiles)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getTasks_async,'task.getTasks')
        yield from self.register(self.createTask_async,'task.createTask')
        yield from self.register(self.updateStatus_async,'task.updateStatus')
        yield from self.register(self.removeTask_async,'task.removeTask')
        yield from self.register(self.removeTaskByStatus_async,'task.removeTaskByStatus')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)



    def getTasks(self, sessionId):
        con = self._getDatabase()
        try:
            userId = self.profiles.getLocalUserId(sessionId)
            return self.task.getTasks(con,userId)
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            con.close()

    @coroutine
    def getTasks_async(self, sessionId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getTasks, sessionId)
        return r



    def createTask(self, sessionId, text):
        con = self._getDatabase()
        try:
            userId = self.profiles.getLocalUserId(sessionId)
            id = self.task.createTask(con,userId,text)
            con.commit()
            task = self.task.find(con,id)
            self.publish('task.newTaskEvent', task)
            return id
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            con.close()

    @coroutine
    def createTask_async(self, sessionId, text):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.createTask, sessionId, text)
        return r



    def updateStatus(self, sessionId, taskId, status):
        con = self._getDatabase()
        try:
            id = self.task.updateStatus(con,taskId,status)
            con.commit()
            task = self.task.find(con,id)
            self.publish('task.changeTaskEvent', task)
            return id
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            con.close()

    @coroutine
    def updateStatus_async(self, sessionId, taskId, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.updateStatus, sessionId, taskId, status)
        return r



    def removeTask(self, sessionId, taskId):
        con = self._getDatabase()
        try:
            userId = self.profiles.getLocalUserId(sessionId)
            id = self.task.removeTask(con,taskId)
            con.commit()
            self.publish('task.removeTaskEvent', id)
            return id
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            con.close()

    @coroutine
    def removeTask_async(self, sessionId, taskId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.removeTask, sessionId, taskId)
        return r



    def removeTaskByStatus(self, sessionId, status):
        con = self._getDatabase()
        try:
            userId = self.profiles.getLocalUserId(sessionId)
            ids = self.task.removeTaskByStatus(con,userId,status)
            con.commit()
            for id in ids:
                self.publish('task.removeTaskEvent', id)
            return id
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            con.close()

    @coroutine
    def removeTaskByStatus_async(self, sessionId, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.removeTaskByStatus, sessionId, status)
        return r
