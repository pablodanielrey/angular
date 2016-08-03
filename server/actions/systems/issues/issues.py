# -*- coding: utf-8 -*-
import inject
import json
import re
import logging
import psycopg2

from model.issue.issue import Issue, RedmineAPI, Attachment, IssueModel
from model.offices.offices import Office

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
    def getMyIssues(self, details):
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
    def getAssignedIssues(self, details):
        con = self.conn.get()
        try:
            userId = self.getUserId(con, details)
            oIds = Office.getOfficesByUser(con, userId, False)
            return Issue.getAssignedIssues(con, userId, oIds)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.find_by_id')
    def findById(self, issue_id, details):
        con = self.conn.get()
        try:
            return Issue.findById(con, issue_id)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.create')
    def create(self, subject, description, parentId, officeId, fromOfficeId, authorId, files, details):
        con = self.conn.get()
        try:
            userId = self.getUserId(con, details)
            authorId = userId if authorId is  None else authorId
            tracker = IssueModel.TRACKER_ERROR
            iss = IssueModel.create(con, parentId, officeId, authorId, subject, description, fromOfficeId, userId, files, tracker)
            con.commit()
            return iss
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.create_comment')
    def createComment(self, subject, description, parentId, projectId, files, details):
        con = self.conn.get()
        try:
            userId = self.getUserId(con, details)
            tracker = IssueModel.TRACKER_COMMENT
            iss = IssueModel.create(con, parentId, projectId, userId, subject, description, '', '', files, tracker)
            con.commit()
            return iss
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.change_status')
    def changeStatus(self, issue, status, details):
        iss = issue.changeStatus(con, status)
        return issue

    @autobahn.wamp.register('issues.change_priority')
    def changePriority(self, issue, priority, details):
        iss = issue.changePriority(con, priority)
        return issue

    @autobahn.wamp.register('issues.get_offices')
    def getOffices(self, details):
        con = self.conn.get()
        try:
            return IssueModel.getOffices(con)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.get_office_subjects')
    def getOfficeSubjects(self, officeId, details):
        return ['Wifi','Otro']

    @autobahn.wamp.register('issues.get_areas')
    def getAreas(self, oId, details):
        con = self.conn.get()
        try:
            return IssueModel.getAreas(con, oId)
        finally:
            self.conn.put(con)
