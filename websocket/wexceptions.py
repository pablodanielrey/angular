# -*- coding: utf-8 -*-


class NullData(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__


class NotImplemented(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__


class MalformedMessage(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__


class UserNotFound(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__


class DupplicatedUser(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__


class MailServerNotFound(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__;


class FailedConstraints(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __init__(self,msg):
        Exception.__init__(self,msg)

    def __str__(self):
        return self.__class__.__name__;


class InsuficientAccess(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__


class AccessDenied(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__
