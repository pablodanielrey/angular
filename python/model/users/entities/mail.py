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
        return ctx.dao(self).persist(ctx, self)

    def delete(self, ctx):
        return ctx.dao(self).delete(ctx, self.id)

    @classmethod
    def findByUserId(cls, ctx, userId):
        return ctx.dao(cls).findByUserId(ctx, userId)

    @classmethod
    def findById(cls, ctx, eid):
        return ctx.dao(cls).findById(ctx, eid)
