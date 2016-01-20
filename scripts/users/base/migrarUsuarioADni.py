# -*- coding: utf-8 -*-
import connection
import connectionLdap
import groups
import users
import systems
import logging

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    import sys
    dni = sys.argv[1]
    name = sys.argv[2]

    ldappass = None
    email = None
    dn = None

    ''' busco a ver si existe el usuario en el ldap y sus propiedades '''
    lcon = connectionLdap.getConnection()
    lcon.search("ou=people,dc=econo", "(uid=" + name + ")", attributes=["uid", 'userPassword', 'mail'])
    result = lcon.entries
    if len(result) > 0:
        n = result[0]
        logging.info(n)
        dn = 'uid={},ou=people,dc=econo'.format(sorted(n.uid)[-1])
        ldappass = str(n.userPassword)
        email = str(n.mail)
    else:
        logging.warn('usuario no existente en el ldap')
    connectionLdap.closeConnection(lcon)

    logging.info(dn)
    logging.info(ldappass)
    logging.info(email)

    assert dn is not None
    assert ldappass is not None
    assert email is not None

    con = connection.getConnection()
    try:
        uid = None

        ''' busco el usuario por el dni '''
        u = users.UserDAO.findByDni(con, dni)
        if u is None:
            logging.warn('Persona inexistente')

            ''' creo el usuario y le pongo la clave que tenga en el ldap '''
            user = users.User()
            user.dni = dni
            user.name = ''
            user.lastname = ''
            uid = users.UserDAO.persist(con, user)

            up = users.UserPassword()
            up.userId = uid
            up.username = dni
            up.password = ldappass
            users.UserPasswordDAO.persist(con, up)

        else:
            ''' le actualizo la clave para que sea la misma que el ldap '''

            (uuid, version) = u
            uid = uuid
            ups = users.UserPasswordDAO.findByUserId(con, uid)
            if len(ups) <= 0:
                ''' creo la clave '''
                up = users.UserPassword()
                up.userId = uid
                up.username = dni
                up.password = ldappass
                users.UserPasswordDAO.persist(con, up)
            else:
                ''' actualizo la clave '''
                up = ups[0]
                up.username = dni
                up.password = ldappass
                users.UserPasswordDAO.persist(con, up)

        ''' le configuro si no tiene email '''
        found = False
        mails = users.MailDAO.findAll(con, uid)
        for m in mails:
            if m.email == email:
                found = True
                break

        if not found:
            ''' no tiene el email configruado asi que se lo creo '''
            m = users.Mail()
            m.userId = uid
            m.email = email
            m.confirmed = True
            users.MailDAO.persist(con, m)

        ''' activo los sistemas para ese usuario '''
        d = systems.Domain()
        d.id = uid
        systems.DomainDAO.persist(con, d)

        ''' imprimo para ver como quedo finalmente '''
        logging.info((lambda x: x.__dict__)(users.UserDAO.findById(con, users.UserDAO.findByDni(con, dni)[0])))
        for m in users.MailDAO.findAll(con, uid):
            logging.info(m.__dict__)
        for u in users.UserPasswordDAO.findByUserId(con, uid):
            logging.info(u.__dict__)

        con.commit()

    finally:
        connection.closeConnection(con)
