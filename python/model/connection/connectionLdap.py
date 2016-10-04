import ldap3
import logging


class Connection:



def getConnection():
    f = open('/tmp/pass.txt')
    try:
        user = f.readline().strip()
        passw = f.readline().strip()

        logging.info('logueandose usando : {} {} al ldap'.format(user, passw))
        server = ldap3.Server('163.10.17.121', use_ssl=False)
        l = ldap3.Connection(server, authentication=ldap3.AUTH_SIMPLE, user=user, password=passw)
        l.open()
        l.bind()

        return l

    finally:
        f.close()


def closeConnection(con):
    con.unbind()
    # con.unbind_s()
