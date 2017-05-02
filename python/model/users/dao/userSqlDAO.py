import datetime
import uuid

from model.dao import SqlDAO
from model.files.entities.file import File
from model.files.dao.fileSqlDAO import FileSqlDAO
from model.users.entities.user import User, Telephone

class UserSqlDAO(SqlDAO):
    ''' DAO usuarios '''

    dependencies = [FileSqlDAO]
    _schema = "profile."
    _table = "users"
    _entity = User

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)
        cur = ctx.con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS profile;

              CREATE TABLE IF NOT EXISTS profile.users (
                id VARCHAR NOT NULL PRIMARY KEY,
                dni VARCHAR NOT NULL UNIQUE,
                name VARCHAR,
                lastname VARCHAR,
                gender VARCHAR,
                birthdate TIMESTAMPTZ,
                city VARCHAR,
                country VARCHAR,
                address VARCHAR,
                type VARCHAR,
                residence_city VARCHAR,
                created TIMESTAMPTZ DEFAULT now(),
                version BIGINT DEFAULT 0,
                photo VARCHAR REFERENCES files.files (id)
              );

              CREATE TABLE IF NOT EXISTS profile.telephones (
                id VARCHAR NOT NULL PRIMARY KEY,
                user_id VARCHAR NOT NULL REFERENCES profile.users (id),
                "number" VARCHAR NOT NULL,
                type VARCHAR
              );
              """

            cur.execute(sql)

        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, u, r):
        u.id = r['id']
        u.dni = r['dni']
        u.name = r['name']
        u.lastname = r['lastname']
        u.gender = r['gender']
        u.birthdate = r['birthdate']
        u.city = r['city']
        u.country = r['country']
        u.address = r['address']
        u.residence_city = r['residence_city']
        u.created = r['created']
        u.version = r['version']
        u.photo = r['photo']
        u.type = r['type']
        return u

    @classmethod
    def _telephoneFromResult(cls, t, r):
        t.id = r['id']
        t.userId = r['user_id']
        t.number = r['number']
        t.type = r['type']
        return t


    @classmethod
    def findByIds(cls, ctx, uids, *args, **kwargs):
        if not uids:
          return []

        cur = ctx.con.cursor()
        try:
            cur.execute('select * from profile.users where id in %s order by lastname, name, dni asc', (tuple(uids),))
            users = []
            for user in cur:
                ouser = cls._fromResult(User(), user)
                cur2 = ctx.con.cursor()
                try:
                    cur2.execute('select * from profile.telephones where user_id = %s', (ouser.id,))
                    ouser.telephones = [ cls._telephoneFromResult(Telephone(), r) for r in cur2 ]
                    users.append(ouser)
                finally:
                    cur2.close()

            return users

        finally:
            cur.close()


    @classmethod
    def search(cls, ctx, regexp):
        """busca ids de usuarios dado una determinada expresión regular"""
        cur = ctx.con.cursor()
        try:
            cur.execute('SELECT id FROM profile.users WHERE '
                        'name ~* %s OR '
                        'lastname ~* %s OR '
                        'dni ~* %s '
                        'LIMIT 50', (regexp, regexp, regexp))
            return [c['id'] for c in cur]

        finally:
            cur.close()

    @classmethod
    def findByType(ctx, types):
        cur = ctx.con.cursor()
        try:
            cur.execute('select id from profile.users where type in %s', (tuple(types),))
            return [c['id'] for c in cur]

        finally:
            cur.close()

    @classmethod
    def findPhoto(cls, ctx, pId):
        f = File.findByIds(ctx, [pId])[0]
        if f is not None:
            content = f.getContent(ctx).tobytes().decode('utf-8')
            f.content = content
        return f

    @classmethod
    def findPhotos(cls, ctx, users):
        if len(users) <= 0:
            return []
        cur = ctx.con.cursor()
        try:
            for user in users:
                cur.execute('select id, photo from profile.users where id = %s', (user.id,))
                pId = cur.fetchone()['photo']
                user.photo = cls.findPhoto(ctx, pId)
            return users
        finally:
            cur.close()

    @classmethod
    def updateType(cls, ctx, userId, type):
        assert userId is not None
        cur = ctx.con.cursor()
        try:
            cur.execute("UPDATE profile.users set type = %s where id = %s", (type, userId))
            return userId
        finally:
            cur.close()


    @classmethod
    def persist(cls, ctx, user):
        cur = ctx.con.cursor()
        try:
            params = user.__dict__

            if not hasattr(user, 'id') or user.id is None:

                params["id"] = str(uuid.uuid4())
                params["version"] = 0
                cur.execute("""
                    INSERT INTO profile.users (id, dni, name, lastname, gender, birthdate, city, country, address, residence_city, version, photo, type)
                    VALUES (%(id)s, %(dni)s, %(name)s, %(lastname)s, %(gender)s, %(birthdate)s, %(city)s, %(country)s, %(address)s, %(residence_city)s, %(version)s, %(photo)s, %(type)s)
                    """, params)

            else:

                cur.execute("""
                    UPDATE profile.users SET
                      dni = %(dni)s,
                      name = %(name)s,
                      lastname = %(lastname)s,
                      gender = %(gender)s,
                      birthdate = %(birthdate)s,
                      city = %(city)s,
                      country = %(country)s,
                      address = %(address)s,
                      residence_city = %(residence_city)s,
                      version = %(version)s,
                      photo = %(photo)s,
                      type =  %(type)s
                    WHERE id = %(id)s
                 """, params)

            cur.execute('delete from profile.telephones where user_id = %s', (params["id"],))
            for t in user.telephones:
                t.id = str(uuid.uuid4())
                t.userId = user.id
                param = t.__dict__
                cur.execute('insert into profile.telephones (id, user_id, number, type) values (%(id)s, %(userId)s, %(number)s, %(type)s)', param)

            return user.id

        finally:
            cur.close()

    @classmethod
    def deleteByIds(cls, ctx, ids):
        cur = ctx.con.cursor()
        try:
            cur.execute("""
               DELETE FROM profile.telephones WHERE user_id IN %s;
               DELETE FROM profile.users
               WHERE id IN %s;
            """, (tuple(ids), tuple(ids)))

        finally:
            cur.close()


class StudentSqlDAO(UserSqlDAO):
    _schema = "students."
    _table = "users"

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)
        cur = ctx.con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS students;
              CREATE TABLE IF NOT EXISTS students.users (
                id VARCHAR PRIMARY KEY NOT NULL REFERENCES profile.users (id),
                student_number VARCHAR UNIQUE,
                condition VARCHAR
              );
              """
            cur.execute(sql)

        finally:
            cur.close()

    @classmethod
    def _fromResult(cls, s, r):
        super()._fromResult(s, r)
        s.id = r['id']
        s.studentNumber = r['student_number']
        s.condition = r['condition']
        return s


    @classmethod
    def findByIds(ctx, ids, *args, **kwargs):
        assert isinstance(ids,list)
        if len(ids) <= 0:
            return []

        cur = con.cursor()
        try:
            cur.execute('select * from students.users su inner join profile.users pu on (pu.id = su.id) where su.id in %s', (tuple(ids),))
            students = [ StudentDAO._fromResult(Student(), s) for s in cur ]
            for s in students:
                cur.execute('select * from profile.telephones where user_id = %s', (s.id,))
                s.telephones = [ cls._telephoneFromResult(Telephone(), r) for r in cur ]

            return students

        finally:
            cur.close()

    @classmethod
    def persist(cls, ctx, student):
        super().persist(ctx, student)

        params = student.__dict__
        cur = con.cursor()
        try:
            cur.execute('select id from students.users where id = %s', (student.id,))
            if cur.rowcount <= 0:
                cur.execute('insert into students.users (id, student_number, condition) values (%(id)s, %(studentNumber)s, %(condition)s)', params)
            else:
                cur.execute('update students.users set student_number = %(studentNumber)s, condition = %(condition)s where id = %(id)s', params)

            return student.id

        finally:
            cur.close()
