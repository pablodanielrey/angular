
class DAO:

    @classmethod
    def _createSchema(cls, con):
        for c in cls.__subclasses__():
            c._createSchema()
