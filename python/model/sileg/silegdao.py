import logging
from model.dao import DAO
from model.sileg.position import *
 
class SilegDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con);
