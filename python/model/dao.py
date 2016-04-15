
class DAO:

    schemaDependencies = []

    @classmethod
    def _createSchema(cls, con):
        for c in cls.__subclasses__():
            for d in c._getDependencies():
                if cls is not d:
                    d._createSchema()

    @classmethod
    def _getDependencies(cls):
        return cls.schemaDependencies
