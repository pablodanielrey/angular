# -*- coding: utf-8 -*-
import uuid
import inject
import hashlib

from model.users.users import Users
from model.mail.mail import Mail
from model.config import Config


class Ingreso:

    users = inject.attr(Users)
    mail = inject.attr(Mail)
    serverConfig = inject.attr(Config)

    """
    def sendFinalEmail(self, con, eid):
        email = self.users.findMail(con, eid)
        if(email is None):
            raise Exception()

        hash = hashlib.sha1(str(uuid.uuid4())).encode('utf-8').hexdigest()
        code = hash[:5]
        email['hash'] = code
        self.users.updateMail(con, email)

        From = self.serverConfig.configs['ingreso_confirm_mail_from']
        subject = self.serverConfig.configs['ingreso_confirm_mail_subject']
        template = self.serverConfig.configs['ingreso_confirm_mail_template']
        To = email['email']

        replace = [
            ('###CODE###', code)
        ]

        self.mail.sendMail(From, [To], subject, replace, html=template)

        return True
    """

    def sendEmailConfirmation(self, con, name, lastname, eid):
        email = self.users.findMail(con, eid)
        if(email is None):
            raise Exception()

        hash = hashlib.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest()
        code = hash[:5]
        email['hash'] = code
        self.users.updateMail(con, email)

        From = self.serverConfig.configs['ingreso_confirm_mail_from']
        subject = self.serverConfig.configs['ingreso_confirm_mail_subject']
        template = self.serverConfig.configs['ingreso_confirm_mail_template']
        To = email['email']

        replace = [
            ('###CODE###', code),
            ('###NAME###', name),
            ('###LASTNAME###', lastname)
        ]

        self.mail.sendMail(From, [To], subject, replace, html=template)

        return True

    def confirmEmail(self, con, eid, code):

        email = self.users.findMail(con, eid)
        if(email is None):
            raise Exception()

        if email['hash'] == code:
            email['confirmed'] = True
            self.users.updateMail(con, email)
            return True

        return False
