# -*- coding: utf-8 -*-
'''
    implementa el modelo del login de los usuarios
'''
import inject
import re

from model.registry import Registry
from model.login.session import Session
from model.users.users import UserPassword, UserPasswordDAO, User, UserDAO

class Login:

    reg = inject.attr(Registry)
    userPassword = inject.attr(UserPasswordDAO)
    users = inject.attr(Users)

    def login(self, con, username, password):
        assert username is not None
        assert password is not None
        up = self.userPassword.findByUserPassword(con, username, password)
        if up is None:
            return None

        s = Session()
        s.userId = up.userId
        s.username = up.username
        sid = self.sessions.persist(con, s)
        return sid

    def logout(self, con, sid):
        assert sid is not None
        self.session.deleteById(con, sid)

    def touch(self, con, sid):
        assert sid is not None
        self.session.touch(con, sid)


    """
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
    """

    #def _sendEmail(self, con, hash, username):
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


    def changePasswordWithHash(self, con, username, password, hash):
        self.userPassword.resetUserPassword(con, hash, username, password)
        return True
    """
