# -*- coding: utf-8 -*-
import inject
import json
import re
import logging
import psycopg2

from model.registry import Registry
from model.connection.connection import Connection

from model.login.login import Login
from model.issue.issue import Issue, RedmineAPI, Attachment, IssueModel
from model.offices.offices import Office

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.serializer.utils import  JSONSerializable

class IssueWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        registry = inject.instance(Registry)
        self.reg = registry.getRegistry('dcsys')
        self.conn = Connection(self.reg)

        self.loginModel = inject.instance(Login)
        self.issueModel = inject.instance(IssueModel)

    @coroutine
    def onJoin(self, details):
        yield from self.register(self.getMyIssues_async, 'issue.getMyIssues')
        yield from self.register(self.getOfficesIssues_async, 'issue.getOfficesIssues')
        yield from self.register(self.getAssignedIssues_async, 'issue.getAssignedIssues')
        yield from self.register(self.findById_async, 'issue.findById')
        yield from self.register(self.create_async, 'issue.create')
        yield from self.register(self.createComment_async, 'issue.createComment')
        yield from self.register(self.changeStatus_async, 'issue.changeStatus')
        yield from self.register(self.getOffices_async, 'issue.getOffices')
        yield from self.register(self.getAreas_async, 'issue.getAreas')


    def getMyIssues(self, sid):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            return Issue.getMyIssues(con, userId)
        finally:
            self.conn.put(con)

    @coroutine
    def getMyIssues_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getMyIssues, sid)
        return r


    def getOfficesIssues(self, sid):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            oIds = Office.getOfficesByUser(con, userId, False)
            return Issue.getOfficesIssues(con, oIds)
        finally:
            self.conn.put(con)

    @coroutine
    def getOfficesIssues_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOfficesIssues, sid)
        return r

    def getAssignedIssues(self, sid):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            oIds = Office.getOfficesByUser(con, userId, False)
            return Issue.getOfficesIssues(con, userId, oIds)
        finally:
            self.conn.put(con)

    @coroutine
    def getAssignedIssues_async(self, sid):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getAssignedIssues, sid)
        return r

    def findById(self, sid, issue_id):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            return Issue.findById(con, userId, issue_id)
        finally:
            self.conn.put(con)

    @coroutine
    def findById_async(self, sid, issue_id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findById, sid, issue_id)
        return r

    def create(self, sid, subject, description, parentId, officeId, fromOfficeId, authorId, files):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            authorId = userId if authorId is  None else authorId
            tracker = self.issueModel.TRACKER_ERROR
            iss = self.issueModel.create(con, parentId, officeId, authorId, subject, description, fromOfficeId, userId, files, tracker)
            con.commit()
            return iss
        finally:
            self.conn.put(con)

    @coroutine
    def create_async(self, sid, subject, description, parentId, officeId, fromOfficeId, authorId, files):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.create, sid, subject, description, parentId, officeId, fromOfficeId, authorId, files)
        return r

    def createComment(self, sid, subject, description, parentId, projectId, files):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            tracker = self.issueModel.TRACKER_COMMENT
            iss = self.issueModel.create(con, parentId, projectId, userId, subject, description, '', '', files, tracker)
            con.commit()
            return iss
        finally:
            self.conn.put(con)

    @coroutine
    def createComment_async(self, sid, subject, description, parentId, projectId, files):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.createComment, sid, subject, description, parentId, projectId, files)

        return r

    def changeStatus(self, sid, issue, status):
        con = self.conn.get()
        try:
            userId = self.loginModel.getUserId(con, sid)
            iss = issue.changeStatus(con, status)
            con.commit()
            return iss
        finally:
            self.conn.put(con)

    @coroutine
    def changeStatus_async(self, sid, issue, status):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.changeStatus, sid, issue, status)
        return r

    def getOffices(self):
        con = self.conn.get()
        try:
            return self.issueModel.getOffices(con)
        finally:
            self.conn.put(con)

    @coroutine
    def getOffices_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOffices)
        return r

    def getAreas(self, oId):
        con = self.conn.get()
        try:
            return self.issueModel.getAreas(con, oId)
        finally:
            self.conn.put(con)

    @coroutine
    def getAreas_async(self, oId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getAreas, oId)
        return r
