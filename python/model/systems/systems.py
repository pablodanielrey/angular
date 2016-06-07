# -*- coding: utf-8 -*-
from model.users.users import StudentDAO
from model.tutorias.tutorias import TutoriasModel
import inject

from model.account.account import AccountModel

class Systems:

    tutorsModel = inject.instance(TutoriasModel)
    accountModel = inject.instance(AccountModel)

    @classmethod
    def listSystems(cls, con, userId):
        systems = []
        if cls._isStudent(con, userId):
            systems.extend(['au24','laboralinsertion','ingreso'])

        if cls._isMail(con, userId):
            systems.extend(['webmail', 'lists', 'digesto'])

        if cls._isOwncloud(con, userId):
            systems.extend(['fcebox'])

        if cls._isAssistance(con, userId):
            systems.extend(['assistance', 'digesto'])

        if cls._isTutors(con, userId):
            systems.extend['tutors']

        if cls._isAccount(con, userId):
            systems.extend(['account'])

        return list(set(systems))

    @classmethod
    def _isStudent(cls, con, userId):
        students = StudentDAO.findById(con, [userId])
        if len(students) <= 0 or students[0] is None:
            return False
        return True

    @classmethod
    def _isMail(cls, con, userId):
        cur = con.cursor()
        try:
            cur.execute('select id from mail.users where id = %s', (userId,))
            return cur.rowcount > 0
        finally:
            cur.close()

    @classmethod
    def _isOwncloud(cls, con, userId):
        cur = con.cursor()
        try:
            cur.execute('select id from owncloud where id = %s', (userId,))
            return cur.rowcount > 0
        finally:
            cur.close()

    @classmethod
    def _isAssistance(cls, con, userId):
        cur = con.cursor()
        try:
            cur.execute('select * from assistance.positions where user_id = %s', (userId,))
            return cur.rowcount > 0
        finally:
            cur.close()

    @classmethod
    def _isTutors(cls, con, userId):
        tutors = cls.tutorsModel.findByTutorId(con, userId)
        if len(tutors) <= 0 or tutors[0] is None:
            return False
        return True

    @classmethod
    def _isAccount(cls, con, userId):
        types = cls.accountModel.getTypes(con, userId)
        if len(types) <= 0:
            return False
        return True
