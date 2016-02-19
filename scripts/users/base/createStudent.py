# -*- coding: utf-8 -*-
'''
    Crea un alumno en la base de datos.
'''

from connection import connection
from users import users
import systems
import logging

def createStudent(dni, name, lastname, studentN):

    logging.getLogger().setLevel(logging.INFO)


    con = connection.getConnection()
    try:
        u = users.UserDAO.findByDni(con, dni)
        if u is not None:
            logging.warn('Persona ya existente')
            logging.warn(u)
            return

        user = users.User()
        user.name = name
        user.lastname = lastname
        user.dni = dni
        uid = users.UserDAO.persist(con, user)

        student = users.Student()
        student.id = uid
        student.studentNumber = studentN
        sid = users.StudentDAO.persist(con, student)

        up = users.UserPassword()
        up.userId = uid
        up.username = dni
        up.password = studentN
        users.UserPasswordDAO.persist(con, up)

        con.commit()

    finally:
        connection.closeConnection(con)


if __name__ == '__main__':

    import sys

    dni = sys.argv[1]
    name = sys.argv[2]
    lastname = sys.argv[3]
    studentN = sys.argv[4]

    assert dni is not None
    assert name is not None
    assert lastname is not None
    assert studentN is not None


    createStudent(dni, name, lastname, studentN)
