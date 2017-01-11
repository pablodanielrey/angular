from model.serializer import JSONSerializable
from model import Ids

class Entity(JSONSerializable):

    def __init__(self):
        super().__init__()

    def persist(self, ctx):
        ctx.dao(self).persist(ctx, self)
        return self

    def delete(self, ctx):
        ctx.dao(self).deleteByIds(ctx, [self.id])
        return self

    @classmethod
    def find(cls, ctx, *args, **kwargs):
        return Ids(cls, ctx.dao(cls).find(ctx, *args, **kwargs))

    @classmethod
    def findByIds(cls, ctx, ids, *args, **kwargs):
        return ctx.dao(cls).findByIds(ctx, ids, *args, **kwargs)
