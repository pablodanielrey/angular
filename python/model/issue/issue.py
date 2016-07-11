# -*- coding: utf-8 -*-
from redmine import Redmine
from model.users.users  import UserPassword, User
from model.offices.offices import Office
from model.serializer.utils import JSONSerializable
from model.registry import Registry

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

    @classmethod
    def create(cls, con, parentId, officeId, authorId, subject, description, fromOfficeId, creatorId):
        issue = Issue()
        issue.parentId = parentId
        issue.projectId = officeId
        issue.userId = authorId
        issue.subject = subject
        issue.description = description
        issue.tracker = RedmineAPI.TRACKER_ERROR
        issue.fromOfficeId = fromOfficeId
        issue.creatorId = creatorId

        return issue.create(con)


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
        self.fromOfficeId = None
        self.creatorId = None

    @classmethod
    def findById(cls, con, userId, id):
        return RedmineAPI.findById(con, userId, id)

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
    KEY = '5f4dbcf2a503728deb879f585c24f00a1b8d6217'
    TRACKER_ERROR = 1
    TRACKER_COMMENT = 4
    STATUS_NEW = 1
    STATUS_WORKING = 2
    STATUS_FINISH = 3
    STATUS_CLOSE = 5
    CREATOR_FIELD = 2
    FROM_FIELD = 3

    @classmethod
    def _loadFile(cls, file):
        att = Attachment()
        att.id = file.id
        att.url = file.content_url
        att.size = file.filesize
        att.name = file.filename
        return att

    @classmethod
    def _fromResult(cls, con, r, redmine):

        attrs = dir(r)
        issue = Issue()
        issue.id = r.id
        issue.parentId = [r.parent.id if 'parent' in attrs else None][0]
        issue.projectId =  [r.project.id if 'project' in attrs else None][0]
        issue.projectName = [r.project.name if 'project' in attrs else None][0]

        issue.userId = cls._loadUserByUIdRedmine(con, r.author.id, redmine)
        issue.subject = r.subject
        issue.description = r.description
        issue.statusId = r.status.id
        issue.assignedToId =[r.assigned_to.id if 'assigned_to' in attrs else None][0]
        issue.start = r.start_date
        issue.updated = r.updated_on

        issue.children = [cls.findById(con, issue.userId, iss.id) for iss in r.children if iss is not None]
        issue.files = [cls._loadFile(file) for file in r.attachments if file is not None]
        return issue



    @classmethod
    def _getRedmineInstance(cls, con, userId):
        ups = UserPassword.findByUserId(con, userId)
        if len(ups) <= 0:
            return None
        up = ups[0]
        redmine = Redmine(cls.REDMINE_URL, key = cls.KEY, version='2.1.2', requests={'verify': False})
        users = redmine.user.filter(name=up.username)
        return (users[0], redmine)

    @classmethod
    def _loadUserByUIdRedmine(cls, con, uid, redmine):
        userRedmine = redmine.user.get(uid)
        dni = userRedmine.login if userRedmine != None and 'login' in dir(userRedmine) else None
        (userId, version) = User.findByDni(con, dni)
        return userId

    @classmethod
    def findById(cls, con, userId, issue_id):
        user, redmine = cls._getRedmineInstance(con, userId)
        if redmine is None:
            return None
        issue = redmine.issue.get(issue_id, include='children, attachments')

        return cls._fromResult(con, issue, redmine)


    @classmethod
    def findAllProjects(cls, con, userId):
        user, redmine = cls._getRedmineInstance(con, userId)
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
        # return [cls._fromResult(con, issue) for issue in issues if not cls._include(issues,issue)]
        return [issue for issue in issues if not cls._include(issues,issue)]


    @classmethod
    def getMyIssues(cls, con, userId):
        user, redmine = cls._getRedmineInstance(con, userId)
        issues = cls._getIssuesByUser(con, user, redmine)
        return [cls._fromResult(con, issue, redmine) for issue in issues if not cls._include(issues,issue)]


    @classmethod
    def _getIssuesByUser(cls, con, user, redmine):
        if redmine is None:
            return []
        issues = redmine.issue.filter(author_id=user.id)
        return issues


    @classmethod
    def getAssignedIssues(cls, con, userId, oIds):
        userRedmine, redmine = cls._getRedmineInstance(con, userId)
        issues = cls._getIssuesByProject(con, oIds, userRedmine, redmine)
        return [cls._fromResult(con, issue, redmine) for issue in issues if not cls._include(issues,issue)]


    @classmethod
    def _getIssuesByProject(cls, con, pidentifiers, user, redmine):
        if redmine is None:
            return []
        issues = []
        for pidentifier in pidentifiers:
            issues.extend(redmine.issue.filter(project_id=pidentifier))

        return issues


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
    def create(cls, con, iss):
        user, redmine = cls._getRedmineInstance(con, iss.userId)
        if redmine is None:
            return None

        issue = redmine.issue.new()

        # ACA FALTA VER EL TEMA DEL USUARIO. PREGUNTARLE A EMA
        issue.project_id = iss.projectId
        issue.subject = iss.subject
        issue.description = iss.description
        issue.status_id = iss.statusId
        issue.parent_issue_id = issue.parentId
        issue.start_date = iss.start
        issue.tracker_id = iss.tracker
        cfields = cls.getCustomFields(iss)
        if len(cfields) > 0:
            issue.custom_fields = cfields
        # issue.uploads = issue.files
        issue.save()

        return True

    @classmethod
    def getCustomFields(cls, issue):
        custom_fields = []
        if issue.creatorId != issue.userId and issue.creatorId is not None:
            custom_fields.append({'id': RedmineAPI.CREATOR_FIELD, 'value': issue.creatorId})
        if issue.fromOfficeId is not None:
            custom_fields.append({'id': RedmineAPI.FROM_FIELD, 'value': issue.fromOfficeId})
        return custom_fields

    @classmethod
    def changeStatus(cls, con, userId, issue_id, project_id, status):
        if status is None:
            return

        if redmine is None:
            return

        user, redmine = cls._getRedmineInstance(con, userId)
        redmine.issue.update(issue_id, status_id = status)
