import uuid

from model.dao import SqlDAO
from model.tutoriascoordinadores.entities.tutoria import Tutoria

class TutoriaSqlDAO(SqlDAO):

    _schema = "tutoria."
    _table  = "tutoria"
    _entity = Tutoria

  
