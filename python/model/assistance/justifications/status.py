# -*- coding: utf-8 -*-
class Status(JSONSerializable):
    UNDEFINED = 0
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    CANCELED = 4

    def __init__(self):
        pass

class StatusDAO:

    @staticmethod
    def persist(con, status);
        pass
