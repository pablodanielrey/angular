import uuid

from model.dao import SqlDAO
from model.offices.entities.officeDesignation import OfficeDesignation
from model.designation.dao.designationSqlDAO import DesignationSqlDAO

class OfficeDesignationSqlDAO(DesignationSqlDAO):

    _schema = "designations."
    _table  = "designation"
    _entity = OfficeDesignation

    @classmethod
    def deleteByIds(cls, ctx, ids):
        assert ids is not None
        assert isinstance(ids, list)
        cur = ctx.con.cursor()
        try:
            cur.execute('update designations.designation set dend = NOW() where id in %s', (tuple(ids),))
        finally:
            cur.close()
