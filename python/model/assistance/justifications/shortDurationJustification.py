
class ShortDurationJustification(JSONSerializable):

    def __init__(self):
        self.id = None
        self.userId = None
        self.start = None
        self.end = None
        self.number = 0

    def persist(self, con):
        ShortDurationJustificationDAO.persist(con, self)


class ShortDurationJustificationDAO:

    @staticmethod
    def _createSchema(con):
        pass

    @staticmethod
    def persist(con, j):
        pass
