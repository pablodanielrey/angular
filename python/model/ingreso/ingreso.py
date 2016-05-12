# -*- coding: utf-8 -*-
import uuid
import inject
import hashlib

from model.users.users import User
import model.users.users
from model.mail.mail import Mail
from model.registry import Registry


class Ingreso:

    registry = inject.instance(Registry)
    reg = registry.getRegistry('ingreso')
    mail = inject.attr(Mail)

    @classmethod
    def sendErrorEmail(cls, error, names, dni, email, tel):
        From = cls.reg.get('error_mail_from')
        subject = "{} - {} - {} - {} - {}".format(error, dni, names, email, tel)
        To = cls.reg.get('error_mail_to')

        mail = cls.mail.createMail(From, To, subject)
        text = cls.mail.getTextPart("error: {}\ndni: {}\nNombres: {}\nEmail: {}\nTel: {}".format(error, dni, names, email, tel))
        mail.attach(text)
        cls.mail._sendMail(From, [To], mail)
        return True

    @classmethod
    def sendFinalEmail(cls, user, password, email):
        From = cls.reg.get('final_mail_from')
        subject = cls.reg.get('final_mail_subject')
        template = cls.reg.get('final_mail_template')
        To = email

        replace = [
            ('###NAME###', user['name']),
            ('###LASTNAME###', user['lastname']),
            ('###PASSWORD###', password),
            ('###USERNAME###', user['dni']),
            ('###EMAIL###', email)
        ]
        cls.mail.sendMail(From, [To, "red@econo.unlp.edu.ar"], subject, replace, html=template)
        return True

    @classmethod
    def sendEmailConfirmation(cls, con, name, lastname, eid):
        emails = model.users.users.Mail.findById(con, eid)
        if emails is None or len(emails) <= 0:
            raise Exception()

        email = emails[0]
        hash = hashlib.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest()
        code = hash[:5]
        email.hash = code
        email.persist(con)

        From = cls.reg.get('confirm_mail_from')
        subject = cls.reg.get('confirm_mail_subject')
        template = cls.reg.get('confirm_mail_template')
        To = email.email

        replace = [
            ('###CODE###', code),
            ('###NAME###', name),
            ('###LASTNAME###', lastname)
        ]
        cls.mail.sendMail(From, [To], subject, replace, html=template)
        return True

    @classmethod
    def checkEmailCode(cls, con, eid, code):
        emails = model.users.users.Mail.findById(con, eid)
        if emails is None or len(emails) <= 0:
            raise Exception()
        return (email[0].hash == code)

    @classmethod
    def confirmEmail(cls, con, eid, code):
        emails = model.users.users.Mail.findById(con, eid)
        if emails is None or len(emails) <= 0:
            raise Exception()

        email = emails[0]
        if email.hash == code:
            email.confirmed = True
            email.persist(con)
            return True

        return False
