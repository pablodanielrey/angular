import re
import uuid
import datetime

from model.offices.entities.office import Office
from model.offices.entities.officeDesignation import OfficeDesignation
from model.users.entities.user import User
from model.serializer import JSONSerializable

class UserOfficeData(JSONSerializable):

    def __init__(self):
        self.id = ''
        self.name = ''
        self.lastname = ''
        self.dni = ''
        self.gender = ''
        self.photo = ''


class OfficeModel():

    @classmethod
    def getOfficesByUser(cls, ctx, userId, tree=False):
        Office.findByUserId(ctx, userId, tree)

    @classmethod
    def persistDesignations(cls, ctx, oid, userIds):
        """
            creo las designaciones para una oficina.
            hay que ver cuales ya existían ya que no se deben tocar las fechas de estas designaciones.
        """
        assert oid is not None
        assert isinstance(userIds, list)

        existent = OfficeDesignation.find(ctx, placeId=[oid], end=True).fetch(ctx)

        if len(userIds) <= 0:
            for d in existent:
                d.delete(ctx)
            return

        toRemove = [d for d in existent if d.userId not in userIds]
        for d in toRemove:
            d.delete(ctx)

        remaining = set(existent) - set(toRemove)
        remainingUsers = [d.userId for d in remaining]
        toGenerate = [u for u in userIds if u not in remainingUsers]

        """ genero y persisto las designaciones adicionales """
        for uid in toGenerate:
            d = OfficeDesignation()
            d.officeId = oid
            d.userId = uid
            d.start = datetime.datetime.now()
            d.persist(ctx)

    @classmethod
    def findOfficesUsers(cls, ctx, oids):
        users = set()
        for oid in oids:
            users.update(cls.getUsers(ctx, oid))
        return list(users)


    @classmethod
    def getUsers(cls, ctx, oId):
        desig = OfficeDesignation.find(ctx, officeId=[oId]).fetch(ctx)
        list(set([d.userId for d in desig]))

    @classmethod
    def searchUsers(cls, ctx, regexp):
        users = User.search(ctx, regexp).fetch(ctx)
        users_ = [cls._getUserData(u) for u in users]
        return users_

    @classmethod
    def findUsersByIds(cls, ctx, uids):
        users = User.findByIds(ctx, uids)
        return [cls._getUserData(ctx, u) for u in users]

    @classmethod
    def _getUserData(cls, ctx, user):
        u = UserOfficeData()
        u.name = user.name
        u.lastname = user.lastname
        u.dni = user.dni
        u.id = user.id
        u.gender = user.gender
        #u.photo = [User.findPhoto(ctx, user.photo) if 'photo' in dir(user) and user.photo is not None and user.photo != '' else None][0]
        return u
