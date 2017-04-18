import uuid

from model.dao import SqlDAO
from model.tutoriascoordinadores.entities.user import User

class CoordinadorSqlDAO(SqlDAO):

    _schema = "tutoring."
    _table  = "coordinador"
    _entity = None

    @classmethod
    def getTutores(cls, ctx, coordinadorId):
        
        sql = """
            SELECT tutor
            FROM coordinador
            WHERE coordinador = %s
        """

        cur = ctx.con.cursor()
        try:
            cur.execute(sql, (tuple(coordinadorId),))
            return [r['tutor'] for r in cur]


        finally:
            cur.close()
