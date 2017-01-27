import uuid

from model.dao import SqlDAO
from model.offices.entities.officeDesignation import OfficeDesignation
from model.designation.dao.designationSqlDAO import DesignationSqlDAO

class OfficeDesignationSqlDAO(DesignationSqlDAO):

    _schema = "designations."
    _table  = "designation_"
    _entity = OfficeDesignation

    @classmethod
    def deleteByIds(cls, ctx, ids):
        assert ids is not None
        assert isinstance(ids, list)
        cur = ctx.con.cursor()
        try:
            cur.execute('UPDATE designations.designation_ set dend = NOW() WHERE id IN %s', (tuple(ids),))
        finally:
            cur.close()
