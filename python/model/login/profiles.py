# -*- coding: utf-8 -*-


class Profile:

    def __init__(self):
        self.userId = None
        self.roles = []


class ProfileDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute('create schema if not exists credentials')
            cur.execute("""
                create table credentials.auth_profile (
                    user_id varchar not null,
                    profile varchar not null
                    created timestamptz default now()
                )
            """)
        finally:
            cur.close()

    @staticmethod
    def findByUserId(con, userId):
        p = Profile()
        p.userId = userId

        cur = con.cursor()
        try:
            roles = []
            cur.execute('select profile from credentails.auth_profile where user_id = %s', (userId,))
            for p in cur:
                profiles.append(p['profile'])
            p.roles = roles

        finally:
            cur.close()

        return p

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
