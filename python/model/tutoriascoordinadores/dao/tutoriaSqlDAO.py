import uuid

from model.dao import SqlDAO
from model.tutoriascoordinadores.entities.Tutoria import Tutoria

class TutoriaSqlDAO(SqlDAO):

    _schema = "tutoria."
    _table  = "tutoria"
    _entity = Tutoria


    // buscar tutorias par coordinador logueado para rol A para tutor B
    def find(para) {
        return consultar(param, condicionobligatioriasessonrolA)
    }
