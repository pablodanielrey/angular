# -*- coding: utf-8 -*-
import logging

from model.entity import Entity
from model.designation.entities.designation import Designation

class Office(Entity):

    officeType = [
        {'value': 'university', 'name': 'Universidad'},
        {'value': 'faculty', 'name': 'Facultad'},
        {'value': 'college', 'name': 'Colegio'},
        {'value': 'unit', 'name': 'Dependencia'},
        {'value': 'secretary', 'name': 'Secretaría'},
        {'value': 'pro-secretary', 'name': 'Pro Secretaría'},
        {'value': 'department', 'name': 'Departamento'},
        {'value': 'direction', 'name': 'Dirección'},
        {'value': 'physical-office', 'name': 'Oficina'},
        {'value': 'intitute', 'name': 'Instituto'},
        {'value': 'magazine', 'name': 'Revista'},
        {'value': 'cdepartment', 'name': 'Cátedra'},
        {'value': 'center', 'name': 'Centro'},
        {'value': 'unity', 'name': 'Unidad'},
        {'value': 'area', 'name': 'Area'},
        {'value': 'group', 'name': 'Grupo'},
        {'value': 'master', 'name': 'Maestría'}
    ]

    def __init__(self):
        self.id = None
        self.name = None
        self.telephone = None
        self.number = None
        self.type = None
        self.email = None
        self.parent = None
        self.public = None
        self.removed = None

    @classmethod
    def getTypes(cls):
        return cls.officeType

    @classmethod
    def findByUser(cls, ctx, userId, types=None, tree=False):
        desig = Designation.find(ctx, userId=[userId]).fetch(ctx)
        oIds = set()
        oIds.update([d.officeId for d in desig])

        if tree:
            childs = set()
            logging.info('buscando hijos')
            for oId in oIds:
                logging.info(oId)
                childs.update(cls.findChildIds(ctx, oId))
                logging.info(childs)
            oIds.update(childs)

        toRemove = []
        if types is not None:
            for off in cls.findByIds(ctx, oIds):
                logging.info('chequeando {}'.format(off))
                logging.info(off.type)
                if off.type is None or off.type['value'] not in types:
                    toRemove.append(off.id)

        return [o for o in oIds if o not in toRemove]


    def findChilds(self, con, types=None, tree=False):
        return ctx.dao(self).findChilds(ctx, self.id, types, tree)
