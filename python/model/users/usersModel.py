# -*- coding: utf-8 -*-
from model.users.entities.user import User
from model.users.entities.userPassword import UserPassword
from model.users.entities.mail import Mail

import model.mail.mail
import hashlib
import inject
import uuid

from model.registry import Registry


class UsersModel():

    mail = inject.attr(model.mail.mail.Mail)


    reg = inject.instance(Registry).getRegistry('mail')

    @classmethod
    def admin(cls, ctx, id):
        user = None
        if id is not None:
            user = User.findById(ctx, id)
            user.types = []
            if user.type:
                types = user.type.split(" ")
                for type in types:
                    t = {"description":type}
                    user.types.append(t)

        if user is None:
            user = User()
            user.types = [];

        return user

    @classmethod
    def persist(cls, ctx, user):
        if not user.types:
            user.type = None
        else:
            types = []
            for t in user.types:
                types.append(t["description"])

            user.type = ' '.join(types)

        user.persist(ctx)
        return user


    @classmethod
    def changePassword(cls, ctx, userId, password):
        user = User.findById(ctx, userId)
        userPasswords = UserPassword.find(ctx, userId=userId, username=user.dni).fetch(ctx)

        up = userPasswords[0] if len(userPasswords) else UserPassword()

        up.userId = user.id
        up.dni = user.dni
        up.password = password
        up.persist(ctx)
        return up

    @classmethod
    def sendEmailConfirmation(cls, ctx, userId, eId):
        user = User.findById(ctx, userId)
        emails = Mail.findByIds(ctx, [eId])
        if emails is None or len(emails) <= 0:
            raise Exception()

        email = emails[0]
        hash = hashlib.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest()
        code = hash[:5]
        email.hash = code
        email.persist(ctx)


        From = cls.reg.get('confirmation_from')
        subject = cls.reg.get('confirmation_subject')
        template = cls.reg.get('confirmation_template')
        #From = "emanuel@econo.unlp.edu.ar"
        #subject = "Prueba de envio"
        #template = "../../python/model/ingreso/templates/codigoActivacion.html"
        To = email.email

        replace = [
            ('###CODE###', code),
            ('###NAME###', user.name),
            ('###LASTNAME###', user.lastname)
        ]
        cls.mail.sendMail(From, [To], subject, replace, html=template)
        return True
