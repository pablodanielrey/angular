from model import Ids
from model.serializer import JSONSerializable

class Mail(JSONSerializable):

    def __init__(self):
        self.id = None
        self.userId = None
        self.email = None
        self.confirmed = False
        self.hash = None
        self.created = None

    def confirm(self, ctx):
        ''' cambia el estado a confirmado '''
        if self.confirmed:
            return
        self.confirmed = True
        return self.persist(ctx)

    def persist(self, ctx):
        ctx.dao(self).persist(ctx, self)
        return self

    def delete(self, ctx):
        ctx.dao(self).delete(ctx, self.id)
        return self

    @classmethod
    def findByIds(cls, ctx, ids):
        return ctx.dao(cls).findByIds(ctx, ids)

    @classmethod
    def findByUserId(cls, ctx, userId):
        return Ids(cls, ctx.dao(cls).findByUserId(ctx, userId))
