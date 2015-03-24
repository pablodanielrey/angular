# -*- coding: utf-8 -*-
import inject, psycopg2

from model.profiles import Profiles
from model.config import Config


class Log:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def __init__(self):
        self.con = None

    def _reconnect(self):
        if self.con == None or self.con.closed != 0:
            self.con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])


    def log(self, msg, sid = None):

        userId = ''
        if sid:
            userId = self.profiles.getLocalUserId(sid)

        self._reconnect()
        cur = self.con.cursor()
        #cur.execute("set time zone %s", ('utc',))
        cur.execute('insert into system.logs (user_id,log) values (%s,%s)',(userId,msg))
        self.con.commit()
