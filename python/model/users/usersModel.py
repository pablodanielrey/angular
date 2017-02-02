# -*- coding: utf-8 -*-
from model.users.entities.user import User
from model.users.entities.userPassword import UserPassword

class UsersModel():
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


    @classmethod
    def changePassword(cls, ctx, userId, password):
        user = User.findById(ctx, userId)
        userPasswords = UserPassword.find(ctx, userId=userId, username=user.dni).fetch(ctx)

        up = userPasswords[0] if len(userPasswords) else UserPassword()

        up.userId = user.id
        up.dni = user.dni
        up.password = password
        up.persist(ctx)
        return up
