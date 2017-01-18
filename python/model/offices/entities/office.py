# -*- coding: utf-8 -*-
from model import Ids
from model.designation.entities.place import Place

class Office(Place):

    def __init__(self):
        super().__init__();
        self.telephone = None
        self.number = None
        self.email = None


    @classmethod
    def findByUserId(cls, ctx, userId, tree=False, *args, **kwargs):
        return Ids(cls, ctx.dao(cls).findByUserId(ctx, userId, tree=False, *args, **kwargs))

    @classmethod
    def findChildsByIds(cls, ctx, ids, tree=False, *args,  **kwargs):
        return Ids(cls, ctx.dao(cls).findChildsByIds(ctx, ids, tree, *args, **kwargs))


    @classmethod
    def persist(cls, ctx, entity):
        if not hasattr(entity, 'id') or entity.id is None:
            entity.id = str(uuid.uuid4())

        aux = cls.findById(ctx, entity.id)

        if aux is not None:
            return cls.update(ctx, entity)

        else:
            return cls.insert(ctx, entity)
