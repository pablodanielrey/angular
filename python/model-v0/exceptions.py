# -*- coding: utf-8 -*-


class NullData(Exception):

    def __init__(self):
        Exception.__init__(self)


class NotImplemented(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __init__(self,msg):
        Exception.__init__(self,msg)


class MalformedMessage(Exception):

    def __init__(self):
        Exception.__init__(self)


class UserNotFound(Exception):

    def __init__(self):
        Exception.__init__(self)


class DupplicatedUser(Exception):

    def __init__(self):
        Exception.__init__(self)


class MailServerNotFound(Exception):

    def __init__(self):
        Exception.__init__(self)


class FailedConstraints(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __init__(self,msg):
        Exception.__init__(self,msg)


class InsuficientAccess(Exception):

    def __init__(self):
        Exception.__init__(self)


class AccessDenied(Exception):

    def __init__(self):
        Exception.__init__(self)
