# -*- coding: utf-8 -*-
import inject
import json
import re
import logging
import psycopg2

from twisted.internet.defer import inlineCallbacks

from model.issue.issue import Issue, RedmineAPI, Attachment, IssueModel
from model.offices.office import Office
from model.users.users import User

#import asyncio
#from asyncio import coroutine
#from autobahn.asyncio.wamp import ApplicationSession

#from model.serializer.utils import  JSONSerializable

import autobahn
import wamp


class Issues(wamp.SystemComponentSession):

    conn = wamp.getConnectionManager()

    def getRegisterOptions(self):
        return autobahn.wamp.RegisterOptions(details_arg='details')

    @autobahn.wamp.register('issues.get_my_issues')
    def getMyIssues(self, statuses, froms, tos, details):
        """
            Obtiene los issues que realizó la oficina de la persona.
            TODO: implementar los filtros.
        """
        con = self.conn.get()
        try:
            userId = self.getUserId(con, details)
            return Issue.getMyIssues(con, userId)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.get_offices_issues')
    def getOfficesIssues(self, details):
        con = self.conn.get()
        try:
            userId = self.getUserId(con, details)
            oIds = Office.getOfficesByUser(con, userId, False)
            return Issue.getOfficesIssues(con, oIds)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.get_assigned_issues')
    def getAssignedIssues(self, statuses, froms, tos, details):
        """
            Retorna los issues asignados a las oficinas a las que pertenece la persona.
        """
        con = self.conn.get()
        try:
            logging.info(statuses)
            logging.info(froms)
            logging.info(tos)

            if statuses is None:
                return []
            assert isinstance(statuses,list)
            if len(statuses) <= 0:
                return []

            userId = self.getUserId(con, details)
            oIds = Office.findByUser(con, userId, types=None, tree=True)
            toIds = [oid for oid in oIds if oid in tos]
            return Issue.getAssignedIssues(con, userId, toIds, froms, statuses)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.find_by_id')
    def findById(self, issueid, details):
        con = self.conn.get()
        try:
            issues = Issue.findByIds(con, [issueid])
            if issues is None or len(issues) <= 0:
                return None
            return issues[0]
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.find_by_ids')
    def findByIds(self, issuesIds, details):
        con = self.conn.get()
        try:
            logging.info(issuesIds)
            if len(issuesIds) <= 0:
                return []
            return Issue.findByIds(con, issuesIds)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.create')
    @inlineCallbacks
    def create(self, subject, description, parentId, officeId, fromOfficeId, authorId, files, details):
        con = self.conn.get()
        try:
            print('create issue')
            userId = self.getUserId(con, details)
            authorId = userId if authorId is  None else authorId
            tracker = IssueModel.TRACKER_ERROR
            issueId = IssueModel.create(con, parentId, officeId, authorId, subject, description, fromOfficeId, userId, files, tracker)
            con.commit()
            print(issueId)
            yield self.publish('issues.issue_created_event', issueId, authorId, fromOfficeId, officeId)
            return issueId
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.create_comment')
    @inlineCallbacks
    def createComment(self, subject, description, parentId, projectId, files, details):
        con = self.conn.get()
        try:
            self.log.info('createComment')
            userId = self.getUserId(con, details)
            tracker = IssueModel.TRACKER_COMMENT
            issueId = IssueModel.create(con, parentId, projectId, userId, subject, description, '', '', files, tracker)
            con.commit()
            yield self.publish('issues.comment_created_event', parentId, issueId)
            return issueId

        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.change_status')
    @inlineCallbacks
    def changeStatus(self, issue, status, details):
        iss = issue.changeStatus(status)
        yield self.publish('issues.updated_event', issue.id, status, issue.priority)
        return issue

    @autobahn.wamp.register('issues.change_priority')
    @inlineCallbacks
    def changePriority(self, issue, priority, details):
        iss = issue.changePriority(priority)
        yield self.publish('issues.updated_event', issue.id, issue.statusId, priority)
        return issue

    @autobahn.wamp.register('issues.get_offices')
    def getOffices(self, details):
        con = self.conn.get()
        try:
            userId = self.getUserId(con, details)
            return IssueModel.getOffices(con, userId)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.search_users')
    def searchUsers(self, regex, details):
        con = self.conn.get()
        try:
            return IssueModel.searchUsers(con, regex)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.get_office_subjects')
    def getOfficeSubjects(self, officeId, details):
        con = self.conn.get()
        try:
            return IssueModel.getSubjectTypes(con, officeId)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.get_areas')
    def getAreas(self, oId, details):
        con = self.conn.get()
        try:
            return IssueModel.getAreas(con, oId)
        finally:
            self.conn.put(con)
