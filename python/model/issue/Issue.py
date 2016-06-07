# -*- coding: utf-8 -*-
from redmine import Redmine
import logging

class IssueModel:

    REDMINE_URL = 'https://redmine-biblio.econo.unlp.edu.ar'

    def _getRedmineInstance(self, userId):
        username = 'admin'
        password = 'lclcynpc'
        self.redmine = Redmine(self.REDMINE_URL, username = 'admin', password = 'lclcynpc', requests={'verify': False})
        return self.redmine

    def getProjects(self):
        redmine = self._getRedmineInstance('1')
        projects = redmine.project.all()
        return projects

    def getIssuesByProject(self, pidentifier):
        redmine = self._getRedmineInstance('1')
        issues = redmine.issue.filter(project_id=pidentifier)
        return issues

    def getIssuesByUser(self, userId):
        redmine = self._getRedmineInstance('1')
        issues = redmine.issue.filter(author_id=userId)
        return issues


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)

    issueModel = IssueModel()
    projects = issueModel.getProjects()
    pidentifier = projects[2].identifier
    # issues = issueModel.getIssuesByProject(pidentifier)
    issues = issueModel.getIssuesByUser('4')
    names = [i.subject for i in issues]

    logging.info('issues {}'.format(names))
