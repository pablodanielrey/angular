
from model.assistance.assistanceDao import AssistanceDAO
from model.users.users import UserDAO

class Boss:

    def __init__(self):
        self.id = None
        self.isBoss = False

    def isBoss(self):
        return self.isBoss

    """
    @classmethod
    def findByUserId(cls, con, userIds, date):
        assert isinstance(userIds, list)
        return BossDAO.findByUserId(con, userIds)
    """

    @classmethod
    def findByUserId(cls, con, userIds, date):
        assert isinstance(userIds, list)
        try:
            return [cls.boss]
        except Exception as e:
            cls.boss = Boss()
            return [cls.boss]

class BossDAO(AssistanceDAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        cur = con.cursor()
        try:
            cur.execute("""
                create schema if not exists assistance;
                create table IF NOT EXISTS assistance.is_boss (
                    id varchar not null primary key references profile.users (id),
                    is_boss boolean default false,
                    created timestamptz default now()
                );
            """)
        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, r):
        b = Boss()
        b.id = r['id']
        b.isBoss = r['is_boss']
        return b

    @classmethod
    def findByUserId(cls, con, userId):
        cur = con.cursor()
        try:
            cur.execute('select * from assistance.is_boss where id in %s', (tuple(userId),))
            return [ cls._fromResult(r) for r in cur ]

        finally:
            cur.close()
