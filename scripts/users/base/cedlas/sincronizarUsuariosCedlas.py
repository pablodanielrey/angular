# -*- coding: utf-8 -*-
'''
    Obtiene los usuarios de la base de datos principal que pertenecen a la oficina Cedlas y los sincroniza con el linux actual.
    Tambien actualiza la clave en el samba
'''
import connection
import users
import groups
import systems
import logging
import datetime
import jsonpickle

if __name__ == '__main__':

    ''' por defecto la fecha de sincronizacion es desde hace un año '''
    lastSinc = datetime.datetime.now() - datetime.timedelta(days=365)
    try:
        with open('/tmp/sinc.dat', 'r') as f:
            lastSinc = jsonpickle.decode(f.read())
    except Exception as e:
        logging.warn(e)

    logging.getLogger().setLevel(logging.INFO)
    con = connection.getConnection()
    try:
        usersToSinc = []
        offices = groups.OfficeDAO.findAll(con)
        for oid in offices:
            office = groups.OfficeDAO.findById(con, oid)
            if office.name == 'Cedlas':
                usersToSinc = office.users
                break

        import subprocess
        from subprocess import PIPE

        for uid in usersToSinc:
            ups = users.UserPasswordDAO.findByUserId(con, uid)
            if len(ups) <= 0:
                continue

            up = ups[0]
            if up.updated <= lastSinc:
                ''' solo lo actualizo si la fecha es mayor a la actual '''
                logging.warn('usuario {} clave ya actualizada {}'.format(up.username, up.updated))
                continue

            logging.info('sincronizando : {}'.format(up.username))

            cmd = 'useradd {}'.format(up.username)
            cp = subprocess.run(cmd, shell=True)
            logging.info(cp.returncode)

            cmd = "echo \"{}:{}\" | chpasswd".format(up.username, up.password)
            cp = subprocess.run(cmd, shell=True)
            logging.info(cp.returncode)

            #cmd = "echo -e \"{1}\n{1}\n\" | smbpasswd -a -s {0}".format(up.username, up.password)
            cmd = "/usr/bin/smbpasswd -a -s {}".format(up.username)
            #logging.info('actualizando clave samba : {}'.format(cmd))
            #cp = subprocess.run(cmd, shell=True)
            cp = subprocess.Popen(['/usr/bin/smbpasswd','-a', '-s', '{}'.format(up.username)], stdout=PIPE, stdin=PIPE, stderr=PIPE, universal_newlines=True)
            o = cp.communicate(input='{0}\n{0}\n'.format(up.password))
            logging.info(cp.returncode)
            logging.info(o)

    finally:
        connection.closeConnection(con)

    ''' almaceno la fecha de la ultima sincronizacion '''
    lastSinc = datetime.datetime.now()
    with open('/tmp/sinc.dat', 'w') as f:
        f.write(jsonpickle.encode(lastSinc))
