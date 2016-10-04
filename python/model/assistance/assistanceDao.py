from model.dao import DAO
 
class AssistanceDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con);
