from model.serializer import JSONSerializable

class UserPassword(JSONSerializable):

    def __init__(self):
        self.id = None
        self.userId = None
        self.username = None
        self.password = None

    def setPassword(self, passw):
        self.password = passw

    def persist(self, ctx):
        return ctx.dao(self).persist(ctx, self)

    @classmethod
    def findByIds(cls, ctx, ids):
        return ctx.dao(cls).findByIds(ctx, ids)

    @classmethod
    def findByUserId(cls, ctx, userId):
        return ctx.dao(cls).findByUserId(ctx, userId)

    @classmethod
    def findByUsername(cls, ctx, username):
        return ctx.dao(cls).findByUsername(ctx, username)

    @classmethod
    def findByUserPassword(cls, ctx, username, password):
        return ctx.dao(cls).findByUserPassword(ctx, username, password)
