from model.serializer import JSONSerializable
from model import Ids

class Entity(JSONSerializable):

    @classmethod
    def findBy(cls, ctx, *args, **kwargs):
        return Ids(cls, ctx.dao(cls).findBy(ctx, *args, **kwargs))
