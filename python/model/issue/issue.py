# -*- coding: utf-8 -*-
from redmine import Redmine
from model.users.users  import UserPassword
from model.offices.offices import Office
from model.serializer.utils import JSONSerializable
import logging
import datetime

class IssueModel():

    @classmethod
    def getOffices(cls, con):
        offices = Office.getOffices(con)
        return Office.findById(con, offices)

    @classmethod
    def getAreas(cls, con, oId):        
        offs = Office.findById(con, [oId])
        if offs is None or len(offs) <= 0:
            return []
        areas = offs[0].getAreas(con)
        return Office.findById(con, areas)


class Issue(JSONSerializable):

    def __init__(self):
        self.id = None
        self.parentId = None
        self.projectId = None
        self.userId = None
        self.subject = ''
        self.description = None
        self.statusId = 1
        self.assignedToId = None
        self.start = datetime.date.today()
        self.updated = None
        self.children = []
        self.files = []
        self.tracker = RedmineAPI.TRACKER_ERROR

    @classmethod
    def findById(cls, con, id):
        return RedmineAPI.findById(con, userId, issue_id)

    @classmethod
    def getOfficesIssues(cls, con, officeIds):
        return RedmineAPI.getOfficesIssues(con, officeIds)

    @classmethod
    def getMyIssues(cls, con, userId):
        return RedmineAPI.getMyIssues(con, userId)

    @classmethod
    def getAssignedIssues(cls, con, userId, oIds):
        return RedmineAPI.getAssignedIssues(con, userId, oIds)

    def changeStatus(self, con, status):
        return RedmineAPI.changeStatus(con, self.userId, self.id, self.projectId, status)

    def create(self, con):
        return RedmineAPI.create(con, self)

class Attachment(JSONSerializable):

    def __init__(self):
        self.id = ''
        self.url = ''
        self.size = 0
        self.name = ''

class RedmineAPI:

    REDMINE_URL = 'https://redmine-biblio.econo.unlp.edu.ar'
    TRACKER_ERROR = 1
    TRACKER_COMMENT = 4
    STATUS_NEW = 1
    STATUS_WORKING = 2
    STATUS_FINISH = 3
    STATUS_CLOSE = 5

    @classmethod
    def _loadFile(cls, file):
        att = Attachment()
        att.id = file.id
        att.url = file.content_url
        att.size = file.filesize
        att.name = file.filename
        return att

    @classmethod
    def _fromResult(cls, r):
        attrs = dir(r)
        issue = Issue()
        issue.id = r.id
        issue.parentId = [r.parent.id if 'parent' in attrs else None][0]
        issue.projectId = r.project.id
        issue.projectName = r.project.name
        issue.userId = r.author.id
        issue.subject = r.subject
        issue.description = r.description
        issue.statusId = r.status.id
        issue.assignedToId =[r.assigned_to.id if 'assigned_to' in attrs else None][0]
        issue.start = r.start_date
        issue.updated = r.updated_on
        issue.children = [iss.id for iss in r.children if iss is not None]
        issue.files = [cls._loadFile(file) for file in r.attachments if file is not None]
        return issue

    @classmethod
    def _getRedmineInstance(cls, con, userId):
        ups = UserPassword.findByUserId(con, userId)
        if len(ups) <= 0:
            return None
        up = ups[0]
        redmine = Redmine(cls.REDMINE_URL, username = up.username, password = up.password, requests={'verify': False})
        return redmine

    @classmethod
    def findById(cls, con, userId, issue_id):
        redmine = cls._getRedmineInstance(con, userId)
        if redmine is None:
            return None
        issue = redmine.issue.get(issue_id, include='children, attachments')
        return cls._fromResult(issue)


    @classmethod
    def findAllProjects(cls, con, userId):
        redmine = cls._getRedmineInstance(con, userId)
        if redmine is None:
            return []
        projects = redmine.project.all()
        return [p.identifier for p in projects]


    @classmethod
    def getOfficesIssues(cls, con, officeIds):
        userIds = Office.getOfficesUsers(con, officeIds)
        issues = []
        for userId in userIds:
            issues.extend(cls.getMyIssues(con, userId))
        return [cls._fromResult(issue) for issue in issues if not cls._include(issues,issue)]


    @classmethod
    def getMyIssues(cls, con, userId):
        issues = cls._getIssuesByUser(con, userId)
        return [cls._fromResult(issue) for issue in issues if not cls._include(issues,issue)]


    @classmethod
    def _include(cls, issues, issue):
        ids = []
        aux = issue

        while 'parent' in dir(aux) and aux.parent:
            ids.append(aux.id)
            aux = aux.parent

        for iss in issues:
            if iss.id in ids:
                return True
        return False


    @classmethod
    def getAssignedIssues(cls, con, userId, oIds):
        issues = cls._getIssuesByProject(con, userId, oIds)
        return [cls._fromResult(issue) for issue in issues if not cls._include(issues,issue)]


    @classmethod
    def _getIssuesByProject(cls, con, userId, pidentifiers):
        redmine = cls._getRedmineInstance(con, userId)
        if redmine is None:
            return []
        issues = []
        for pidentifier in pidentifiers:
            issues.extend(redmine.issue.filter(project_id=pidentifier))

        return issues


    @classmethod
    def _getIssuesByUser(cls, con, userId):
        redmine = cls._getRedmineInstance(con, userId)
        if redmine is None:
            return []
        issues = redmine.issue.filter(author_id=userId)
        return issues

    @classmethod
    def create(cls, con, issue):

        redmine = cls._getRedmineInstance(con, issue.userId)
        if redmine is None:
            return None

        issue = redmine.issue.new()

        issue.project_id = issue.projectId
        issue.subject = issue.subject
        issue.description = issue.description
        issue.status_id = issue.statusId
        issue.parent_issue_id = issue.parentId
        issue.start_date = issue.start
        issue.tracker_id = issue.tracker
        issue.uploads = issue.files
        issue.save()

        return issue

    @classmethod
    def changeStatus(cls, con, userId, issue_id, project_id, status):
        if status is None:
            return

        if redmine is None:
            return

        redmine = cls._getRedmineInstance('1')
        redmine.issue.update(issue_id, status_id = status)
