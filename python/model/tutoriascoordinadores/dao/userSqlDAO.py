import uuid

from model.dao import SqlDAO
from model.tutoriascoordinadores.entities.User import User

class UserSqlDAO(SqlDAO):

    _schema = "profile."
    _table  = "users"
    _entity = User

    @classmethod
    def _fromResult(cls, u, r):
        u.id = r['id']
        u.dni = r['dni']
        u.name = r['name']
        u.lastname = r['lastname']
        return u


    @classmethod
    def findTutores(cls, ctx, coordinadorId):


        sql = """
            SELECT tutor_id
            FROM tutoring.coordinador
            WHERE coordinador_id = %s
        """

        cur = ctx.con.cursor()
        try:
            cur.execute(sql, (coordinadorId,))
            return [r['tutor_id'] for r in cur]


        finally:
            cur.close()

    def getLoggedCordinator():
        return session[userId]
