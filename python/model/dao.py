import logging

class DAO:

    dependencies = []

    @classmethod
    def _createSchema(cls, con):
        print(cls)
        for dep in cls._getDependencies():
            logging.debug('creando schema : {}'.format(dep.__name__))
            dep._createSchema(con)
          
        for c in cls.__subclasses__():
          for d in c._getDependencies():
              if c is not d:
                  logging.debug('creando schema : {}'.format(d.__name__))
                  d._createSchema(con)

    @classmethod
    def _getDependencies(cls):
        return cls.dependencies
        
        
