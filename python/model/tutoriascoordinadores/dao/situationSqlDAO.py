# -*- coding: utf-8 -*-
import uuid

from model.dao import SqlDAO
from model.tutoriascoordinadores.entities.Situation import Situation



class SituationSqlDAO(SqlDAO):

    _schema = "tutoring."
    _table  = "situations"
    _entity = Situation


    @classmethod
    def _fromResult(cls, s, r):
        s.id = r['id']
        s.situation = r['situation']
        s.tutoringId = r['tutoring_id']
        s.userId = r['user_id']

        return s
    
    @classmethod
    def findByIds(cls, ctx, ids, *args, **kwargs):
        orderBy = cls._orderBy(**kwargs)
        o = " ORDER BY {}".format(', ' .join(orderBy)) if len(orderBy) else ""
        sql = "SELECT CONCAT(tutoring_id, '_', user_id) AS id, * FROM {}{} WHERE CONCAT(tutoring_id, '_', user_id) IN %s {};".format(cls._schema, cls._table, o)
        cur = ctx.con.cursor()

        try:
            cur.execute(sql, (tuple(ids),))
            return [cls._fromResult(cls._entity(), c) for c in cur ]

        finally:
            cur.close()

    @classmethod
    def find(cls, ctx, *args, **kwargs):
        condition = cls._condition(**kwargs)
        orderBy = cls._orderBy(**kwargs)

        c = " WHERE {}".format(' AND ' .join(condition["list"])) if len(condition["list"]) else ""
        o = " ORDER BY {}".format(', ' .join(orderBy)) if len(orderBy) else ""
        sql = "SELECT CONCAT(tutoring_id, '_', user_id) AS id FROM {}{}{}{};".format(cls._schema, cls._table, c, o)

        cur = ctx.con.cursor()
        try:
            cur.execute(sql, tuple(condition["values"]))

            if cur.rowcount <= 0:
                return []

            return [r['id'] for r in cur]

        finally:
            cur.close()
