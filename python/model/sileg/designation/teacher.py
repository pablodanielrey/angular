# -*- coding: utf-8 -*-
from model.sileg.designation import DesignationDAO


class TeacherDesignationDAO(DesignationDAO):
    
    dependencies = [TeacherPositionDAO, CathedraPlaceDAO]
    
    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS sileg;

              CREATE TABLE IF NOT EXISTS sileg.teacher_designation (
                    id VARCHAR PRIMARY KEY,
                    user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                    position_id VARCHAR NOT NULL REFERENCES sileg.teacher_position (id),
                    place_id VARCHAR NOT NULL REFERENCES sileg.cathedra_place (id),
                    dfrom DATE,
                    dto DATE,
                    created TIMESTAMPTZ DEFAULT now()
              );
              """
            cur.execute(sql)
        finally:
            cur.close()
            
   


class TeacherDesignation(TeacherDesignationDAO):
  pass
