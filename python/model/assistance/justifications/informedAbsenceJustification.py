
from model.dao import DAO
from model.assistance.justifications.justifications import Justification


class InformedAbsence(Justification):

    def __init__(self, userId, ownerId, date):
        super().__init__(date, userId, ownerId)

    def getIdentifier(self):
        return "Ausente con aviso"


class InformedAbsenceDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        pass

    @staticmethod
    def persist(con, ia):
        pass
