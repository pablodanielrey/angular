# -*- coding: utf-8 -*-
'''
    implementa el modelo del login de los usuarios
'''
import inject
import re

from model.registry import Registry
from model.login.session import Session, SessionDAO
from model.login.profiles import Profile, ProfileDAO
from model.users.users import UserPassword, UserPasswordDAO, User, UserDAO, UserModel

class Login:

    reg = inject.attr(Registry)
    userPassword = inject.attr(UserPasswordDAO)
    users = inject.attr(UserModel)
    sessions = inject.attr(SessionDAO)
    profiles = inject.attr(ProfileDAO)

    def hasRoles(self, con, sId, roles = []):
        ss = self.sessions.findById(con, [sId])
        if len(ss) <= 0:
            return False

        jprofile = ss[0].data
        if jprofile is None:
            return False

        return Profile._fromJson(jprofile).hasRoles(roles)

    def hasOneRole(self, con, sId, roles = []):
        ss = self.sessions.findById(con, [sId])
        if len(ss) <= 0:
            return False

        jprofile = ss[0].data
        if jprofile is None:
            return False

        return Profile._fromJson(jprofile).hasOneRole(roles)

    def getUserId(self, con, sId):
        assert con is not None
        assert sId is not None
        ss = self.sessions.findById(con, [sId])
        return ss[0].userId

    def testUser(self, con, username):
        assert username is not None
        up = self.userPassword.findByUsername(con, username)
        return len(up) > 0

    def login(self, con, username, password):
        assert username is not None
        assert password is not None
        up = self.userPassword.findByUserPassword(con, username, password)
        if up is None:
            return None

        s = Session()
        s.userId = up.userId
        s.username = up.username

        profile = self.profiles.findByUserId(con, s.userId)
        if profile is not None:
            s.data = profile._toJson()

        sid = self.sessions.persist(con, s)
        s.id = sid
        return s

    def logout(self, con, sid):
        assert sid is not None
        self.sessions.deleteById(con, sid)

    def touch(self, con, sid):
        assert sid is not None
        self.sessions.touch(con, sid)
