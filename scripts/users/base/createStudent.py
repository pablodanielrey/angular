# -*- coding: utf-8 -*-
'''
    Crea un alumno en la base de datos.

    PYTHONPATH="../../../python" python3 createStudent.py dni name lastname legajo
'''

from model.connection import connection
from model.users import users
from model.registry import Registry
import systems
import logging

def createStudent(con, dni, name, lastname, studentN):

    logging.getLogger().setLevel(logging.INFO)

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


if __name__ == '__main__':

    import inject
    inject.configure()

    import sys

    dni = sys.argv[1]
    name = sys.argv[2]
    lastname = sys.argv[3]
    studentN = sys.argv[4]

    assert dni is not None
    assert name is not None
    assert lastname is not None
    assert studentN is not None

    r = inject.instance(Registry)
    conn = connection.Connection(r.getRegistry('dcsys'))
    con = conn.get()
    try:
        createStudent(con, dni, name, lastname, studentN)
        con.commit()

    finally:
        conn.put(con)
