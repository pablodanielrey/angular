#-*- coding: utf -*-
"""
    sincroniza los usuarios del owncloud
    usa la librería :
        https://github.com/owncloud/pyocclient
"""

import sys
assert sys.version_info >= (2,7)
import logging
logging.getLogger().setLevel(logging.INFO)

def getUsersToSync(duser, dpassword):
    import psycopg2
    con = psycopg2.connect(database='dcsys', user=duser, password=dpassword, host='127.0.0.1', port=5432)
    try:
        con.set_session(isolation_level=psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED, readonly=True)
        cur = con.cursor()
        try:
            cur.execute(
                    "select username, password from credentials.user_password where updated <= NOW() - INTERVAL '5 days'"
                    " and "
                    "user_id in (select pu.id from profile.users pu, profile.mails pm where pu.id = pm.user_id and pm.email like '%econo.unlp.edu.ar%' and pm.confirmed)"
                )
            return [(r[0],r[1]) for r in cur]
        finally:
            cur.close()
    finally:
        con.close()
    return []

def syncUsersToOwncloud(ocuser, ocpassw, users):
    import owncloud
    oc = owncloud.Client('https://owncloud.econo.unlp.edu.ar', verify_certs = False, single_session = True)
    oc.login(ocuser, ocpassw)
    try:
        for u, password in users:
            logging.info('Actualizando {}'.format(u))
            if not oc.user_exists(u):
                oc.create_user(u,password)
            else:
                oc.set_user_attribute(u,'password',password)

    finally:
        oc.logout()


if __name__ == '__main__':

    duser = sys.argv[1]
    dpassw = sys.argv[2]

    ocuser = sys.argv[3]
    ocpassw = sys.argv[4]

    users = getUsersToSync(duser, dpassw)
    syncUsersToOwncloud(ocuser, ocpassw, users)
