import re
import uuid
import datetime

from model.offices.office import Office
from model.designation.designation import Designation
from model.users.users import User
from model.offices.userIssueData import UserIssueData
from model.serializer import JSONSerializable

class UserOfficeData(JSONSerializable):

    def __init__(self):
        self.id = ''
        self.name = ''
        self.lastname = ''
        self.dni = ''
        self.photo = ''


class OfficeModel():

    @classmethod
    def getOfficesByUser(cls, ctx, userId, types=None, tree=False):
        Office.findByUser(ctx, userId, types, tree)

    @classmethod
    def persistDesignations(cls, ctx, oid, userIds):
        """
            creo las designaciones para una oficina.
            hay que ver cuales ya existían ya que no se deben tocar las fechas de estas designaciones.
        """
        assert oid is not None
        assert isinstance(userIds, list)

        eids = Designation.findByOffice(ctx, oid, history=False)
        existent = Designation.findByIds(ctx, eids)

        if len(userIds) <= 0:
            """ elimino todas las deisgnaciones """
            for d in existent:
                d.expire(ctx)
            return

        toRemove = [d for d in existent if d.userId not in userIds]

        """ elimno las designaciones que no deberían existir """
        for d in toRemove:
            d.expire(ctx)

        remaining = set(existent) - set(toRemove)
        remainingUsers = [d.userId for d in remaining]
        toGenerate = [u for u in userIds if u not in remainingUsers]

        """ genero y persisto las designaciones adicionales """
        for uid in toGenerate:
            d = Designation()
            d.id = str(uuid.uuid4())
            d.officeId = oid
            d.userId = uid
            d.start = datetime.datetime.now()
            d.persist(con)

    @classmethod
    def findOfficesUsers(cls, ctx, oids):
        users = set()
        for oid in oids:
            users.update(cls.getUsers(ctx, oid))
        return list(users)

    @classmethod
    def getUsers(cls, ctx, oId):
        idsD = Designation.findByOffice(ctx, oId)
        desig = Designation.findByIds(ctx, idsD)
        uIds = set()
        uIds.update([d.userId for d in desig])
        return list(uIds)

    @classmethod
    def searchUsers(cls, ctx, regexp):
        ids = User.search(ctx, regexp)
        users = [cls._getUserData(uid) for uid in ids]
        return users

    @classmethod
    def findUsersByIds(cls, con, uids):
        users = User.findById(con, uids)
        return [cls._getUserData(con, u) for u in users]

    @classmethod
    def _getUserData(cls, con, user):
        u = UserOfficeData()
        u.name = user.name
        u.lastname = user.lastname
        u.dni = user.dni
        u.id = user.id
        u.gender = user.gender
        u.photo = [User.findPhoto(con, user.photo) if 'photo' in dir(user) and user.photo is not None and user.photo != '' else None][0]
        return u
