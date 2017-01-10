from model.dao import Ids
from model.serializer import JSONSerializable


class Telephone(JSONSerializable):
    def __init__(self):
        self.id = None
        self.userId = None
        self.number = None
        self.type = None


class User(JSONSerializable):
    ''' usuario básico del sistema '''

    def __init__(self):
        self.id = None
        self.dni = None
        self.name = None
        self.lastname = None
        self.gender = None
        self.birthdate = None
        self.city = None
        self.country = None
        self.address = None
        self.residence_city = None
        self.created = datetime.datetime.now()
        self.version = 0
        self.photo = None
        self.type = None
        self.telephones = []
        self.type = None

    def getAge(self):
        today = datetime.datetime.now()
        born = self.birthdate
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def persist(self, ctx):
        ctx.dao(self).persist(ctx, self)
        return self

    def delete(self, ctx):
        ctx.dao(self).deleteById(ctx, [self.id])
        return self

    def updateType(self, ctx):
        ctx.dao(self).updateType(ctx, self.id, self.type)
        return self

    @classmethod
    def findByIds(cls, ctx, ids):
        assert isinstance(ids, list)
        return ctx.dao(cls).findByIds(ctx, ids)

    @classmethod
    def search(cls, ctx, regex):
        return Ids(cls, ctx.dao(cls).search(con, regex))

    @classmethod
    def findAll(cls, ctx):
        return Ids(cls, ctx.dao(cls).findAll(ctx))

    @classmethod
    def findByType(cls, ctx, types):
        return Ids(cls, ctx.dao(cls).findByType(ctx, types))

    @classmethod
    def findByDnis(cls, ctx, dnis):
        return Ids(cls, ctx.dao(cls).findByDni(ctx, dnis))



    @classmethod
    def findPhoto(cls, ctx, pId):
        return ctx.dao(cls).findPhoto(ctx, pId)

    @classmethod
    def findPhotos(cls, ctx, userIds):
        return ctx.dao(cls).findPhotos(ctx, userIds)


class Student(User):

    def __init__(self):
        super().__init__()
        self.studentNumber = None
        self.condition = None

    def persist(self, ctx):
        ctx.dao(self).persist(ctx, self)
        return self
