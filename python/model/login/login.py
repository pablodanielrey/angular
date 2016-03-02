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
    users = inject.attr(User)

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
