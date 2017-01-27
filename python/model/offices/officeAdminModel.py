import re
import uuid
import datetime

from model.offices.entities.office import Office
from model.users.entities.user import User
from model.offices.entities.officeDesignation import OfficeDesignation


class OfficeAdminModel():
    @classmethod
    def admin(cls, ctx, id):
        office = None
        if id is not None:
            office = Office.findById(ctx, id)

        if office is None:
            office = Office()

        return office

    @classmethod
    def searchUsers(cls, ctx, search):
        users = User.search(ctx, search).fetch(ctx)
        users_ = []
        for u in users:
            user = {
                id: u.id,
                label: u.name + " " + u.lastname + " " + u.dni
            }
            users_.append(user)

        return users_

    @classmethod
    def getDesignations(cls, ctx, placeId):
        designations = OfficeDesignation.find(ctx, placeId=placeId).fetch(ctx)

        for d in designations:
            user = User.findById(ctx, d.userId)
            user.id = u.id
            user.label = u.name + " " + u.lastname + " " + u.dni
            users_.append(user)

        return designations
