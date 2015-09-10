# -*- coding: utf-8 -*-
import inject

from model.config import Config
from model.credentials.credentials import UserPassword
from model.session import Session


class Login:

    config = inject.attr(Config)
    session = inject.attr(Session)
    userPassword = inject.attr(UserPassword)

    def login(self, con, username, password):
        credentials = {
            'username': username,
            'password': password
        }
        rdata = self.userPassword.findUserPassword(con, credentials)
        if rdata is None:
            return None

        sess = {
            self.config.configs['session_user_id']: rdata['user_id']
        }
        sid = self.session._create(con, sess)

        response = {'session_id': sid, 'user_id': rdata['user_id']}
        return response

    def logout(self, con, sid):
        ''' sess = self.session._findSession(con, sid) '''
        self.session._destroy(con, sid)

    def generateResetPasswordHash(self, con, username):
        hash = ''
        return hash

    def changePasswordWithHash(con, username, password, hash):
        return True
