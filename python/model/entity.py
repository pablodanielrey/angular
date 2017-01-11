from model.serializer import JSONSerializable
from model import Ids

class Entity(JSONSerializable):

    @classmethod
    def findBy(cls, ctx):
        ctx.dao(cls)
        #return Ids(cls, ctx.dao(cls).findBy(ctx, *args, **kwargs))
