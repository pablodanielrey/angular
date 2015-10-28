# -*- coding: utf-8 -*-
import logging
import psycopg2
import sys
import smtplib
from email.mime.text import MIMEText


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    if len(sys.argv) <= 4:
        logging.warn('argumentos insuficientes')
        logging.warn('usuariodb clavedb dni usuarioau24')
        sys.exit(1)

    user = sys.argv[1]
    passw = sys.argv[2]

    dni = sys.argv[3]
    username = sys.argv[4]

    con = psycopg2.connect(host='163.10.17.80', dbname='au24', user=user, password=passw)
    try:
        cur = con.cursor()

        logging.info('chequeando si existe {}'.format(username))
        cur.execute('select username from mdl_user where username = %s', (username,))
        if cur.rowcount <= 0:
            logging.info('no existe usuario {}, por lo que no tengo que actualizar nada'.format(username))
            sys.exit()

        logging.info('chequeando si existe {}'.format(dni))
        cur.execute('select username from mdl_user where username = %s', (dni,))
        if cur.rowcount >= 0:
            logging.info('actualizando {0} a {0}.viejo'.format(dni))
            cur.execute("update mdl_user set auth = %s, username = %s where username = %s", ('fceldap', '{}.viejo'.format(dni), dni))

        logging.info('actualizando {} a {}'.format(username, dni))
        cur.execute("update mdl_user set auth = %s, username = %s where username = %s", ('fceldap', dni, username))
        con.commit()

    finally:
        con.close()

    text = 'usuario actualizado del au24 : {} --> {}'.format(username, dni)
    msg = MIMEText(text)
    msg['Subject'] = text
    msg['From'] = 'pablo@econo.unlp.edu.ar'
    msg['To'] = 'pablo@econo.unlp.edu.ar, anibal.alvarez@econo.unlp.edu.ar, soporte@econo.unlp.edu.ar'
    s = smtplib.SMTP('163.10.17.115')
    try:
        s.send_message(msg)

    finally:
        s.quit()
