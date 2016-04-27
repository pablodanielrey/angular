import logging

class DAO:

    dependencies = []

    @classmethod
    def _createSchema(cls, con):
        for dep in cls._getDependencies():
            logging.debug('creando schema : {}'.format(dep.__name__))
            dep._createSchema(con)
          
        for c in cls.__subclasses__():
            logging.debug('creando schema : {}'.format(c.__name__))
            c._createSchema(con)
   
    @classmethod
    def _getDependencies(cls):
        return cls.dependencies
        
        
        
        
