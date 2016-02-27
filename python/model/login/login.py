# -*- coding: utf-8 -*-
import inject
import re

from model.registry import Registry
from model.users.users import UserPassword, UserPasswordDAO, User, UserDAO

from model.session import Session
from model.mail.mail import Mail



class Login:

    config = inject.attr(Registry)
    session = inject.attr(Session)
    userPassword = inject.attr(UserPasswordDAO)
    users = inject.attr(Users)
    mail = inject.attr(Mail)

    def login(self, con, username, password):
        rdata = self.userPassword.findByUserPassword(con, username, password)
        if rdata is None:
            return None

        sess = {
            self.config.configs['session_user_id']: rdata['user_id'],
            self.config.configs['session_user_username']: rdata['username']
        }
        sid = self.session._create(con, sess)

        response = {'session_id': sid, 'user_id': rdata['user_id']}
        return response

    def logout(self, con, sid):
        ''' sess = self.session._findSession(con, sid) '''
        self.session._destroy(con, sid)

    def _sendEmail(self, con, hash, username):
        ''' envío el hash a todos los mails que tenga confirmado el usuario '''

        """
            variables a reemplazar :
            ###DNI###
            ###NAME###
            ###LASTNAME###
            ###URL###

            y estas en a url.
            ###HASH###
            ###USERNAME###
        """

        creds = self.userPassword.findCredentials(con, username)
        user_id = creds['user_id']
        user = self.users.findUser(con, user_id)
        mails = self.users.listMails(con, user_id)
        emails = [x['email'] for x in mails if x['confirmed'] == True]

        if len(emails) <= 0:
            raise Exception('No tienen ningún email confirmado')

        url = self.config.configs['mail_reset_password_url']
        url = re.sub('###HASH###', hash, url)
        url = re.sub('###USERNAME###', username, url)

        From = self.config.configs['mail_reset_password_from']
        subject = self.config.configs['mail_reset_password_subject']
        template = self.config.configs['mail_reset_password_template']

        replace = [
            ('###DNI###', user['dni']),
            ('###NAME###', user['name']),
            ('###LASTNAME###', user['lastname']),
            ('###URL###', url)
        ]

        self.mail.sendMail(From, emails, subject, replace, html=template)

        return True

    def generateResetPasswordHash(self, con, username):
        hash = self.userPassword.getResetPasswordHash(con, username)
        self._sendEmail(con, hash, username)
        return hash

    def changeUserPassword(self, con, sid, username, password):
        sess = self.session._getSession(con, sid)
        if sess is None:
            return False

        if sess['username'] is not username:
            return False

        creds = self.userPassword.findCredentials(con, username)
        creds['password'] = password
        self.userPassword.updateUserPassword(con, creds)
        return True

    def changePasswordWithHash(self, con, username, password, hash):
        self.userPassword.resetUserPassword(con, hash, username, password)
        return True
