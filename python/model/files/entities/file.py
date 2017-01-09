import hashlib
from model.serializer import JSONSerializable

class File(JSONSerializable):

    @staticmethod
    def _calculateHashStatic(content):
        m = hashlib.md5()
        m.update(content.encode('utf8'))
        return m.hexdigest()

    @classmethod
    def getContentById(cls, ctx, cId):
        return ctx.dao(cls).getContentById(ctx, cId)

    def __init__(self):
        self.id = None
        self.name = None
        self.hash = None
        self.content = None
        self.mimetype = None
        self.codec = None
        self.size = 0
        self.created = None
        self.modified = None

    def _calculateHash(self):
        self.hash = File._calculateHashStatic(self.content)

    def getContent(self, ctx):
        return self.getContentById(ctx, self.id)

    @classmethod
    def findByIds(cls, ctx, ids):
        return ctx.dao(cls).findByIds(ctx, ids)

    @classmethod
    def exists(cls, ctx, id):
        return ctx.dao(cls).exists(ctx, id)
