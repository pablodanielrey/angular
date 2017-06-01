
class Identifier:

    internal = {}
    identifiers = {}

    @classmethod
    def put(cls, uid, id):
        cls.internal[uid] = id
        cls.identifiers[id] = uid

    @classmethod
    def getInternal(cls, uid):
        return cls.internals[uid]

    @classmethod
    def getUid(cls, id):
        return cls.identifiers[id]
