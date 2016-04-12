
class DAO:
    dependencies = []
    
    @classmethod
    def _createSchema(cls, con):
        for c in cls.__subclasses__():
            c._createSchema()
            
    @classmethod
    def _createDependencies(cls, con):
        for c in cls.dependencies:
            c._createSchema(con)
