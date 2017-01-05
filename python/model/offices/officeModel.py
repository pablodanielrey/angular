from model.designation.designation import Designation
from model.users.users import User
from model.offices.userIssueData import UserIssueData
from model.offices.office import Office

import re
import uuid
import datetime





class OfficeModel():

    cache = {}

    @classmethod
    def getOfficesByUser(cls, con, userId, types=None, tree=False):
        Office.findByUser(con, userId, types, tree)

    @classmethod
    def persistDesignations(cls, con, oid, userIds):
        """
            creo las designaciones para una oficina.
            hay que ver cuales ya existían ya que no se deben tocar las fechas de estas designaciones.
        """
        assert oid is not None
        assert isinstance(userIds, list)

        eids = Designation.findByOffice(con, oid, history=False)
        existent = Designation.findByIds(con, eids)

        if len(userIds) <= 0:
            """ elimino todas las deisgnaciones """
            for d in existent:
                d.expire(con)
            return

        toRemove = [d for d in existent if d.userId not in userIds]

        """ elimno las designaciones que no deberían existir """
        for d in toRemove:
            d.expire(con)

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
    def findOfficesUsers(cls, con, oids):
        users = set()
        for oid in oids:
            users.update(cls.getUsers(con, oid))
        return list(users)

    @classmethod
    def getUsers(cls, con, oId):
        idsD = Designation.findByOffice(con, oId)
        desig = Designation.findByIds(con, idsD)
        uIds = set()
        uIds.update([d.userId for d in desig])
        return list(uIds)

    @classmethod
    def searchUsers(cls, con, regex):
        assert regex is not None

        if regex == '':
            return []

        userIds = User.findAll(con)

        users = []
        for u in userIds:
            (uid, version) = u
            if uid not in cls.cache.keys():
                user = User.findById(con, [uid])[0]
                cls.cache[uid] = user
            users.append(cls.cache[uid])

        m = re.compile(".*{}.*".format(regex), re.I)
        matched = []

        digits = re.compile('^\d+$')
        if digits.match(regex):
            ''' busco por dni '''
            matched = [ cls._getUserData(con, u) for u in users if m.search(u.dni) ]
            return matched

        ''' busco por nombre y apellido '''
        matched = [ cls._getUserData(con, u) for u in users if m.search(u.name) or m.search(u.lastname) or m.search(u.name + u.lastname) or m.search(u.lastname + u.name)]
        return matched

    @classmethod
    def findUsersByIds(cls, con, uids):
        users = User.findById(con, uids)
        return [cls._getUserData(con, u) for u in users]

    @classmethod
    def _getUserData(cls, con, user):
        u = UserIssueData()
        u.name = user.name
        u.lastname = user.lastname
        u.dni = user.dni
        u.id = user.id
        u.genre = user.genre
        u.photo = [User.findPhoto(con, user.photo) if 'photo' in dir(user) and user.photo is not None and user.photo != '' else None][0]
        return u
