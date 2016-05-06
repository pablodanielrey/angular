# -*- coding: utf-8 -*-
import re
import uuid
from model.dao import DAO
from model.users.users import UserDAO, User, StudentDAO, Student

class TutoringSituation:

    def __init__(self):
        self.userId = None
        self.user = None
        self.situation = None


class Tutoring:

    def __init__(self):
        self.id = None
        self.date = None
        self.tutorId = None
        self.tutor = None
        self.situations = []

    def _loadTutor(self, con):
        self.tutor = UserDAO.findById(con, [self.tutorId])[0]

    def _loadStudents(self, con):
        for ss in self.situations:
            ss.user = {
                'user': UserDAO.findById(con, [ss.userId])[0],
                'student': StudentDAO.findById(con, [ss.userId])[0]
            }

    @classmethod
    def findAll(cls, con):
        return TutoringDAO.findAll(con)

class TutoringDAO(DAO):

    dependencies = [UserDAO]

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()

        try:
            cur.execute("""
                create schema if not exists tutoring;

                create table if not exists tutoring.tutorings (
                    id varchar primary key,
                    tutor_id varchar not null references profile.users (id),
                    date timestamptz default now(),
                    created timestamptz default now()
                );
                create table if not exists tutoring.situations (
                    tutoring_id varchar not null references tutoring.tutorings (id),
                    user_id varchar not null references profile.users (id),
                    situation varchar not null
                );
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        t = Tutoring()
        t.id = r['id']
        t.date = r['date']
        t.tutorId = r['tutor_id']
        return t

    @staticmethod
    def _situationFromResult(r):
        s = TutoringSituation()
        s.situation = r['situation']
        s.userId = r['user_id']
        return s

    @staticmethod
    def persist(con, tutoring):
        cur = con.cursor()
        try:
            if tutoring.id is None:
                tutoring.id = str(uuid.uuid4())
            else:
                cur.execute('delete from tutoring.situations where tutoring_id = %s', (tutoring.id,))
                cur.execute('delete from tutoring.tutorings where id = %s', (tutoring.id,))

            params = tutoring.__dict__
            cur.execute('insert into tutoring.tutorings (id, tutor_id, date) values (%(id)s, %(tutorId)s, %(date)s)', params)

            for s in tutoring.situations:
                params = s.__dict__
                params['tutoringId'] = tutoring.id
                cur.execute('insert into tutoring.situations (tutoring_id, situation, user_id) values (%(tutoringId)s, %(situation)s, %(userId)s)', params)

            return tutoring.id

        finally:
            cur.close()

    @staticmethod
    def delete(con, tid):
        cur = con.cursor()
        try:
            cur.execute('delete from tutoring.situations where tutoring_id = %s', (tid,))
            cur.execute('delete from tutoring.tutorings where id = %s', (tid,))
            return (cur.rowcount > 0)

        finally:
            cur.close()

    @classmethod
    def findAll(cls, con):
        cur = con.cursor()
        try:
            tutorings = []
            cur.execute('select * from tutoring.tutorings')
            for c in cur.fetchall():
                tutoring = TutoringDAO._fromResult(c)

                cur.execute('select * from tutoring.situations where tutoring_id = %s', (tutoring.id,))
                for c2 in cur:
                    tutoring.situations.append(TutoringDAO._situationFromResult(c2))

                tutoring._loadTutor(con)
                tutoring._loadStudents(con)
                tutorings.append(tutoring)

            return tutorings

        finally:
            cur.close()

    @staticmethod
    def findByTutorId(con, tId):
        cur = con.cursor()
        try:
            tutorings = []
            cur.execute('select * from tutoring.tutorings where tutor_id = %s', (tId,))
            for c in cur.fetchall():
                tutoring = TutoringDAO._fromResult(c)

                cur.execute('select * from tutoring.situations where tutoring_id = %s', (tutoring.id,))
                for c2 in cur:
                    tutoring.situations.append(TutoringDAO._situationFromResult(c2))

                tutoring._loadTutor(con)
                tutoring._loadStudents(con)
                tutorings.append(tutoring)

            return tutorings

        finally:
            cur.close()


class TutoriasModel:

    def __init__(self):
        self.cache = {}

    def persist(self, con, tutoring):
        return TutoringDAO.persist(con, tutoring)

    def delete(self, con, tid):
        return TutoringDAO.delete(con, tid)

    def findByTutorId(self, con, tId):
        return TutoringDAO.findByTutorId(con, tId)

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

        import copy
        m = re.compile(".*{}.*".format(regex), re.I)
        matched = []
        if '/' in regex:
            ''' busco por número de alumnos '''
            matched = [ copy.deepcopy(u) for u in users if u['student'].studentNumber != None and m.search(u['student'].studentNumber) ]
            return matched

        digits = re.compile('^\d+$')
        if digits.match(regex):
            ''' busco por dni '''
            matched = [ copy.deepcopy(u) for u in users if m.search(u['user'].dni) ]
            return matched

        ''' busco por nombre y apellido '''
        matched = [ copy.deepcopy(u) for u in users if m.search(u['user'].name) or m.search(u['user'].lastname) ]
        return matched
