
class OfficeDAO:

    @classmethod
    def findChilds(cls, ctx, oid, types=None, tree=False):
        raise NotImplementedError()

    @classmethod
    def findAll(cls, ctx, types=None):
        raise NotImplementedError()

    @classmethod
    def persist(cls, ctx, office):
        raise NotImplementedError()

    @classmethod
    def remove(cls, ctx, id):
        raise NotImplementedError()
