import uuid

from model.dao import SqlDAO
from model.tutoriascoordinadores.entities.Tutoria import Tutoria

class TutoriaSqlDAO(SqlDAO):

    _schema = "tutoring."
    _table  = "tutorings"
    _entity = Tutoria


    @classmethod
    def _fromResult(cls, t, r):
        t.id = r['id']
        t.tutorId = r['tutor_id']
        t.date = r['date']
        return t
