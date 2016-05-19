# -*- coding: utf-8 -*-
'''
    implementa el modelo del login de los usuarios
'''
import inject
import re
import hashlib
import uuid
from model.registry import Registry
from model.login.session import Session
from model.login.profiles import Profile
# from model.users.users import UserPassword, UserPasswordDAO, User, UserDAO, UserModel
from model.users.users import UserPassword, User, Mail


class LoginMail:
    """
        Implementa el envío de mails necesario para el reset de clave.
        config dentro del registry.cfg necesaria.

        [login]
        confirm_mail_from = ditise@econo.unlp.edu.ar
        confirm_mail_subject = Confirmación de cambio de clave.
        confirm_mail_template = /ruta/a/python/model/login/templates/codigoActivacion.html

        final_mail_from = ditise@econo.unlp.edu.ar
        final_mail_subject = Datos de cuenta
        final_mail_template = /ruta/a/python/model/login/templates/bienvenida.html
    """

    registry = inject.instance(Registry)
    reg = registry.getRegistry('login')

    from model.mail.mail import Mail
    mail = inject.attr(Mail)

    @classmethod
    def sendFinalEmail(cls, user, password, email):
        From = cls.reg.get('final_mail_from')
        subject = cls.reg.get('final_mail_subject')
        template = cls.reg.get('final_mail_template')
        To = email

        replace = [
            ('###NAME###', user.name),
            ('###LASTNAME###', user.lastname),
            ('###PASSWORD###', password),
            ('###USERNAME###', user.dni),
            ('###EMAIL###', email)
        ]
        cls.mail.sendMail(From, [To, "red@econo.unlp.edu.ar"], subject, replace, html=template)
        return True

    @classmethod
    def sendEmailConfirmation(cls, con, name, lastname, eid):
        emails = Mail.findById(con, eid)
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


class ResetPassword:

    mail = LoginMail

    @classmethod
    def findByDni(cls, con, dni):
        data = User.findByDni(con, dni)
        if data is None:
            raise Exception()

        uid, version = data
        user = User.findById(con, [uid])[0]

        mails = Mail.findByUserId(con, uid)
        """ busco el primer alternativo """
        mail = None
        for m in mails:
            if 'econo.unlp.edu.ar' not in m.email:
                 mail = m
                 break

        if mail is None:
            raise Exception()

        if cls.mail.sendEmailConfirmation(con, user.name, user.lastname, m.id):
            return (user, m)
        else:
            raise Exception()

    @classmethod
    def checkEmailCode(cls, con, eid, code):
        emails = Mail.findById(con, eid)
        if emails is None or len(emails) <= 0:
            raise Exception()
        for email in emails:
            if emails[0].hash == code:
                return True
        return False

    @classmethod
    def resetPassword(cls, con, uid, dni, eid, code, password):
        """
            resetea la clave siempre y cuando los parámetros coincidan con los datos de la base
        """
        email = None
        emails = Mail.findById(con, eid)
        if emails is None or len(emails) <= 0:
            raise Exception()

        for e in emails:
            if e.hash == code:
                email = e
                break

        if email is None:
            raise Exception()

        if cls.checkEmailCode(con, eid, code):
            user = User.findById(con, [uid])[0]
            ups = UserPassword.findByUserId(con, uid)
            for up in ups:
                if up.username == dni:
                    up.setPassword(password)
                    up.persist(con)
                    cls.mail.sendFinalEmail(user, password, email.email)
                    return True
        return False


class Login:

    reg = inject.attr(Registry)

    def hasRoles(self, con, sId, roles = []):
        ss = Session.findById(con, [sId])
        if len(ss) <= 0:
            return False

        jprofile = ss[0].data
        if jprofile is None:
            return False

        return Profile._fromJson(jprofile).hasRoles(roles)

    def hasOneRole(self, con, sId, roles = []):
        ss = Session.findById(con, [sId])
        if len(ss) <= 0:
            return False

        jprofile = ss[0].data
        if jprofile is None:
            return False

        return Profile._fromJson(jprofile).hasOneRole(roles)

    def getUserId(self, con, sId):
        assert con is not None
        assert sId is not None
        ss = Session.findById(con, [sId])
        return ss[0].userId

    def testUser(self, con, username):
        assert username is not None
        up = UserPassword.findByUsername(con, username)
        return len(up) > 0

    def login(self, con, username, password):
        assert username is not None
        assert password is not None
        up = UserPassword.findByUserPassword(con, username, password)
        if up is None:
            return None

        s = Session()
        s.userId = up.userId
        s.username = up.username

        profile = Profile.findByUserId(con, s.userId)
        if profile is not None:
            s.data = profile._toJson()

        sid = s.persist(con)
        s.id = sid
        return s

    def logout(self, con, sid):
        assert sid is not None
        Session.deleteById(con, sid)

    def touch(self, con, sid):
        assert sid is not None
        Session.touch(con, sid)
