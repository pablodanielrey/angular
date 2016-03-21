# -*- coding: utf-8 -*-

import re
from model.users.users import UserDAO, User, StudentDAO, Student

class TutoriasModel:

    def __init__(self):
        self.cache = {}

    def search(self, con, regex):
        assert regex is not None

        if regex == '':
            return []

        userIds = StudentDAO.findAll(con)

        users = []
        for uid in userIds:
            if uid not in self.cache.keys():
                user = {
                    'user': UserDAO.findById(con, [uid])[0],
                    'student': StudentDAO.findById(con, [uid])[0]
                }
                self.cache[uid] = user
            users.append(self.cache[uid])

        m = re.compile(".*{}.*".format(regex), re.I)
        matched = []
        if '/' in regex:
            ''' busco por número de alumnos '''
            matched = [ u for u in users if u['student'].studentNumber != None and m.search(u['student'].studentNumber) ]
            return matched

        digits = re.compile('^\d+$')
        if digits.match(regex):
            ''' busco por dni '''
            matched = [ u for u in users if m.search(u['user'].dni) ]
            return matched

        ''' busco por nombre y apellido '''
        matched = [ u for u in users if m.search(u['user'].name) or m.search(u['user'].lastname) ]
        return matched
