
from model.serializer.utils import JSONSerializable
import datetime

from model.dao import DAO
from model.users.users import UserDAO
import uuid
import logging


class PositionDAO(DAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS position;

              create table IF NOT EXISTS assistance.positions (
                  id varchar primary key,
                  user_id varchar not null references profile.users (id),
                  name varchar not null
              );
              """
            cur.execute(sql)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, r):
        p = Position(r['user_id'], r['name'])
        return p

    @classmethod
    def findByUser(cls, con, userIds):
        assert isinstance(userIds, list)

        if len(userIds) <= 0:
            return

        cur = con.cursor()
        try:
            logging.info('userIds: %s', tuple(userIds))
            cur.execute('select * from assistance.positions where user_id in %s',(tuple(userIds),))
            return [ cls._fromResult(r) for r in cur ]
        finally:
            cur.close()



class Position(JSONSerializable):

    dao = PositionDAO

    def __init__(self, userId, name):
        self.userId = userId
        self.name = name


    @classmethod
    def findByUser(cls, con, userIds):
        return cls.dao.findByUser(con, userIds)
