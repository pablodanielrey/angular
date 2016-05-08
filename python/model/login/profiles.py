# -*- coding: utf-8 -*-
import json
from model.dao import DAO
from model.users.users import UserDAO

class Profile:

    def __init__(self):
        self.userId = None
        self.roles = []

    def hasOneRole(self, role = []):
        if len(role) <= 0:
            return False

        if len(role) == 1:
            return role[0] in self.roles

        for r in role:
            if r in self.roles:
                return True
        return False

    def hasRoles(self, role = []):
        if len(role) <= 0:
            return False

        if len(role) == 1:
            return role[0] in self.roles

        for r in role:
            if r not in self.roles:
                return False
        return True

    def _toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def _fromJson(pstring):
        p = Profile()
        p.__dict__ = json.loads(pstring)
        return p

class ProfileDAO(DAO):

    dependencies = [UserDAO]
    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists credentials;
                
                create table IF NOT EXISTS credentials.auth_profile (
                    user_id varchar not null REFERENCES profile.users (id),
                    profile varchar not null,
                    created timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @staticmethod
    def findByUserId(con, userId):
        profile = Profile()
        profile.userId = userId

        cur = con.cursor()
        try:
            roles = []
            cur.execute('select profile from credentials.auth_profile where user_id = %s', (userId,))
            for p in cur:
                roles.append(p['profile'])
            profile.roles = roles

        finally:
            cur.close()

        return profile

    @staticmethod
    def persist(con, profiles = []):
        if len(profiles) <= 0:
            return

        cur = con.cursor()
        try:
            for p in profiles:
                param = p.__dict__
                cur.execute('insert into credentials.auth_profile (user_id, profile) select (%(userId)s, %(profile)s) where not exists (select user_id from credentials.auth_profile where user_id = %(userId)s and profile = %(profile)s)', param)

        finally:
            cur.close()

    @staticmethod
    def remove(con, profiles = []):
        if len(profiles) <= 0:
            return

        cur = con.cursor()
        try:
            for p in profiles:
                param = p.__dict__
                cur.execute('delete from credentials.auth_profile where user_id = %(userId)s and profile = %(profile)s)', param)

        finally:
            cur.close()
