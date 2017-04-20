import uuid

from model.dao import SqlDAO
from model.tutoriascoordinadores.entities.Student import Student


class StudentSqlDAO(SqlDAO):

    _schema = "students."
    _table  = "users"
    _entity = Student
