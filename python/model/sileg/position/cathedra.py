# -*- coding: utf-8 -*-
from model.sileg.position import *


class CathedraPositionDAO(PositionDAO):
    
    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS sileg;

              CREATE TABLE IF NOT EXISTS sileg.cathedra_position (
                    id VARCHAR PRIMARY KEY,
                    cathedra VARCHAR NOT NULL REFERENCES cathedra.users (id),
                    dedication VARCHAR NOT NULL
              );
              """
            cur.execute(sql)
        finally:
            cur.close()
            
   


class TeacherDesignation(TeacherDesignationDAO):
  pass
