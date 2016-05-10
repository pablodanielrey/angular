# -*- coding: utf-8 -*-
import logging
import unittest
import sys
sys.path.append('../../python')

from testecono.TestEcono import TestEcono
from model.users.users import User
from model.users.users import Telephone
from model.users.users import UserDAO

from random import randint


class TestUser(TestEcono):

    def setUp(self):
        super(TestUser, self).setUp()
        try:
            con = self.connection.get()
            try:
                UserDAO._createSchema(con)
                con.commit()

            finally:
                self.connection.put(con)

        except Exception as e:
            logging.error(str(e))

    @classmethod
    def defineUser(cls):
        telephone = Telephone()
        telephone.type = "Móvil"
        telephone.number = str(randint(40000000,50000000))

        dni = str(randint(30000000,40000000))
        user = User()
        user.name = "Test Nom " + dni
        user.lastname = "Test Ape " + dni
        user.dni = dni
        user.telephones = [ telephone ]

        return user

    @classmethod
    def defineUserAndPersist(cls, con):
        user = cls.defineUser()

        u = User.findByDni(con, user.dni)

        if u is not None:
            user.id = u[0]

        uid = user.persist(con)

        return uid, user





    def assertEqualTelephones(self, telephone, telephone2):
        self.assertEqual(telephone.type, telephone2.type)


    def assertEqualUsers(self, user, user2):
        self.assertEqual(user.name, user2.name)
        self.assertEqual(user.lastname, user2.lastname)
        self.assertEqual(user.dni, user2.dni)
        self.assertEqual(len(user.telephones), len(user2.telephones))
        for t1, t2 in zip(user.telephones, user2.telephones):
           self.assertEqualTelephones(t1,t2)





class TestUserPersist(TestUser):

    def setUp(self):
        super(TestUserPersist, self).setUp()
        try:
            con = self.connection.get()
            self.user = TestUserPersist.defineNewUser(con)
            con.commit()

        finally:
            self.connection.put(con)



    @classmethod
    def defineNewUser(cls, con):
        user = TestUserPersist.defineUser()

        uid = User.findByDni(con, user.dni)

        if(uid is not None):
          users = User.findById(con, [uid[0]])
          u = users[0]
          u.delete(con)

        return user


    def test_persist(self):
        try:
            con = self.connection.get()
            try:

                ##### insertar #####
                self.user.persist(con)
                con.commit()
                uid = User.findByDni(con, self.user.dni)
                u = User.findById(con, [uid[0]])
                self.assertEqualUsers(self.user, u[0])


                ##### actualizar #####
                self.user.name = "Test Nomb " + self.user.dni
                self.user.persist(con)
                con.commit()
                uid = User.findByDni(con, self.user.dni)
                u = User.findById(con, [uid[0]])

                self.assertEqualUsers(self.user, u[0])

                ##### error #####
                user = self.defineUser()
                user.dni = self.user.dni
                with self.assertRaises(Exception):
                    UserDAO.persist(con, user)

            finally:
                self.connection.put(con)

        except Exception as e:
            logging.error(str(e))









class TestUserFindById(TestUser):

    def setUp(self):
        super(TestUserFindById, self).setUp()
        try:
            con = self.connection.get()
            self.user_id, self.user = TestUserFindById.defineUserAndPersist(con)
            con.commit()

        finally:
            self.connection.put(con)


    def test_find_by_id(self):
        try:
            con = self.connection.get()
            try:
                u = User.findById(con,[self.user.id])
                self.assertEqualUsers(self.user, u[0])

                u = User.findById(con, ["not_exists"])
                self.assertEqual(u, [])


            finally:
                self.connection.put(con)

        except Exception as e:
            logging.error(str(e))









class TestUserFindAll(TestUser):

    def setUp(self):
        super(TestUserFindAll, self).setUp()
        try:
            con = self.connection.get()
            self.user_id, self.user = TestUserFindById.defineUserAndPersist(con)
            con.commit()

        finally:
            self.connection.put(con)



    def test_find_all(self):
        try:
            con = self.connection.get()
            uTuple = (self.user_id, self.user.version)
            try:
                u = User.findAll(con)
                self.assertIn(uTuple, u)

                uTupleNotExists = ("id", "0")
                self.assertNotIn(uTupleNotExists, u)


            finally:
                self.connection.put(con)

        except Exception as e:
            logging.error(str(e))







class TestUserDelete(TestUser):

    def setUp(self):
        super(TestUserDelete, self).setUp()
        try:
            con = self.connection.get()
            self.user_id, self.user = TestUserFindById.defineUserAndPersist(con)
            con.commit()

        finally:
            self.connection.put(con)



    def test_delete(self):
        try:
            con = self.connection.get()

            try:
                self.user.delete(con)
                con.commit()

                u = User.findById(con, [self.user_id])
                self.assertEqual(u, [])

            finally:
                self.connection.put(con)

        except Exception as e:
            logging.error(str(e))



if __name__ == '__main__':
    unittest.main()
