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
