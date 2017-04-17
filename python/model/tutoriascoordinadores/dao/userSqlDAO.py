import uuid

from model.dao import SqlDAO
from model.tutoriascoordinadores.entities.user import User

class UserSqlDAO(SqlDAO):

    _schema = "profile."
    _table  = "users"
    _entity = User


