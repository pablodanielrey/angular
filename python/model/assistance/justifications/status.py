# -*- coding: utf-8 -*-
from model.serializer.utils import JSONSerializable
import datetime

class Status(JSONSerializable):
    UNDEFINED = 0
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    CANCELED = 4

    def __init__(self, jid):
        self.created = datetime.datetime.now()
        self.status = Status.PENDING
        self.id = None
        self.justificationId = jid
        self.userId = None

    def persist(self, status):
        pass

class StatusDAO:

    @staticmethod
    def persist(con, status);
        pass
