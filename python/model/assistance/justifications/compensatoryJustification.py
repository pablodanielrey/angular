
from model.dao import DAO
from model.assistance.justifications.justifications import SingleDateJustification


class CompensatoryDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        cur = con.cursor()
        try:
            pass
        finally:
            cur.close()

    @staticmethod
    def _fromResult(con, r):
        pass

    @staticmethod
    def persist(con, ia):
        pass

    @staticmethod
    def findById(con, ids):
        assert isinstance(ids, list)
        pass

    @staticmethod
    def findByUserId(con, userIds, start, end):
        assert isinstance(userIds, list)
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)
        pass

class Compensatory(SingleDateJustification):

    def __init__(self, userId, ownerId, date):
        super().__init__(date, userId, ownerId)

    def getIdentifier(self):
        return "Compensatorio"
