# -*- coding: utf-8 -*-

from model.users.entities.user import User


class UsersAdminModel():

    @classmethod
    def admin(cls, ctx, id):
        user = None
        if id is not None:
            user = User.findById(ctx, id)
            user.types = []
            if user.type:
                types = user.type.split(" ")
                for type in types:
                    t = {"description":type}
                    user.types.append(t)

        if user is None:
            user = User()
            user.types = [];

        return user

    @classmethod
    def persist(cls, ctx, user):
        if not user.types:
            user.type = None
        else:
            types = []
            for t in user.types:
                types.append(t["description"])

            user.type = ' '.join(types)

        user.persist(ctx)
        return user
