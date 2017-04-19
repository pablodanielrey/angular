import uuid

from model.dao import SqlDAO
from model.tutoriascoordinadores.entities.user import User

class UserSqlDAO(SqlDAO):

    _schema = "profile."
    _table  = "users"
    _entity = User




    @classmethod
    def getTutores(cls, ctx, coordinadorId):
        
        sql = """
            SELECT tutor_id
            FROM coordinador
            WHERE coordinador_id = %s
        """

        cur = ctx.con.cursor()
        try:
            cur.execute(sql, (tuple(coordinadorId),))
            return [r['tutor'] for r in cur]


        finally:
            cur.close()

