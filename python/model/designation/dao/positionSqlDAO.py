# -*- coding: utf-8 -*-
from model.dao import DAO
import uuid

class PositionDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS designations;

                CREATE TABLE IF NOT EXISTS designations.positions (
                  id VARCHAR PRIMARY KEY,
                  position VARCHAR,
                  type INTEGER,
                  created TIMESTAMPTZ default now()
                );
            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, r):
        d = Position()
        d.id = r['id']
        d.position = r['position']
        d.type = r['type']
        return d

    @classmethod
    def findByIds(cls, con, ids):
        assert ids is not None

        if len(ids) <= 0:
            return []

        cur = con.cursor()
        try:
            cur.execute('select * from designations.positions where id in %s', (tuple(ids),))
            if cur.rowcount <= 0:
                return []

            return [PositionDAO._fromResult(o) for o in cur.fetchall()]

        finally:
            cur.close()

    """
        TODO: HACK HORRIBLE PARA MANTENER FUNCIONANOD CODIGO DE ASISTENCIA Y OTROS SISTEMAS QUE
        SUPONEN 1 SOLO CARGO ACTIVO, POR ESO LO BUSCAN USANDO Position.findByUserId() Y NO Designations
    """
    @classmethod
    def findByUserId(cls, con, userId):
        cur = con.cursor()
        try:
            cur.execute("""
              SELECT dp.* from designations.positions dp
              INNER JOIN designations.designation dd ON (dd.position_id = dp.id)
              WHERE dd.position_id = dp.id
              AND dd.user_id = %s
              ORDER BY dstart DESC
              LIMIT 1;
            """, (userId,));

            return [cls._fromResult(r) for r in cur]
        finally:
            cur.close()
