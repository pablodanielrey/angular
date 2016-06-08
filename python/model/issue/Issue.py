# -*- coding: utf-8 -*-
from redmine import Redmine
import logging
import datetime

class IssueModel:

    REDMINE_URL = 'https://redmine-biblio.econo.unlp.edu.ar'
    TRACKER_ERROR = 1
    TRACKER_COMMENT = 4
    STATUS_NEW = 1
    STATUS_WORKING = 2
    STATUS_FINISH = 3
    STATUS_CLOSE = 5

    def _getRedmineInstance(self, userId):
        username = 'admin'
        password = 'lclcynpc'
        self.redmine = Redmine(self.REDMINE_URL, username = username, password = password, requests={'verify': False})
        return self.redmine

    def _getProjects(self):
        redmine = self._getRedmineInstance('1')
        projects = redmine.project.all()
        return projects

    def getMyIssues(self, userId):
        issues = []
        # busco

    def _getIssuesByProject(self, pidentifier):
        redmine = self._getRedmineInstance('1')
        issues = redmine.issue.filter(project_id=pidentifier)
        return issues

    def _getIssuesByUser(self, userId):
        redmine = self._getRedmineInstance(userId)
        issues = redmine.issue.filter(author_id=userId)
        return issues

    def findById(self, issue_id):
        redmine = self._getRedmineInstance('1')
        issue = redmine.issue.get(issue_id, include='children, attachments')
        return issue

    def create(self, officeId, subject, description = '', parentId = None, tracker = TRACKER_ERROR, start = None, statusId = 1, files = []):
        if start is None:
            start = datetime.date.today()

        redmine = self._getRedmineInstance('1')
        issue = redmine.issue.new()
        issue.project_id = officeId
        issue.subject = subject
        issue.description = description
        issue.status_id = statusId
        issue.parent_issue_id = parentId
        issue.start_date = start
        issue.tracker_id = tracker
        # issue.uploads = [{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
        issue.uploads = files
        issue.save()

        return issue


    def changeStatus(self, issue_id, project_id, status):
        if status is None:
            return

        redmine = self._getRedmineInstance('1')
        redmine.issue.update(issue_id, status_id = status)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)

    issueModel = IssueModel()
    projects = issueModel._getProjects()
    pidentifier = projects[2].identifier
    # issues = issueModel.getIssuesByProject(pidentifier)
    issues = issueModel._getIssuesByUser('4')
    names = [i.subject for i in issues]
    logging.info('issues {}'.format(names))

    issue = issueModel.create(pidentifier, 'prueba python', 'estoy probando la creacion')
    child = issueModel.create(pidentifier, 'prueba hijo', 'subtarea', issue.id, issueModel.TRACKER_COMMENT)

    issue_id = issue.id
    issue = issueModel.findById(issue_id)
    logging.info('issue: {}'.format(issue.__dict__))

    issueModel.changeStatus(issue_id, pidentifier, issueModel.STATUS_WORKING)
