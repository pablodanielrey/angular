import uuid

from model.dao import SqlDAO
from model.tutoriascoordinadores.entities.Situation import Situation


class SituationSqlDAO(SqlDAO):

    _schema = "tutoring."
    _table  = "situations"
    _entity = Situation


    @classmethod
    def _fromResult(cls, s, r):
        s.situation = r['situation']
        s.tutoringId = r['tutoring_id']
        s.userId = r['user_id']

        return s
