#-*- coding: utf -*-

'''
    invocación:

    PYTHONPATH=../../python python3 rechazados.py
'''

from model.registry import Registry
import imaplib
import inject
import logging
import sys

if __name__ == '__main__':

    inject.configure()

    logging.getLogger().setLevel(logging.INFO)

    reg = inject.instance(Registry)
    m = imaplib.IMAP4_SSL('163.10.17.115')
    try:
        u = reg.get('imap_user')
        p = reg.get('imap_pass')
        logging.info('logueandose usando {}'.format(u))
        rv, data = m.login(u, p)
        logging.info('{} {}'.format(rv, data))
        rv, mailboxes = m.list()
        if rv != 'OK':
            logging.info(rv)
            sys.exit(1)
        #logging.info(mailboxes)

        rv, data = m.select('grupos/soportecampus')
        if rv != 'OK':
            sys.exit(1)
        logging.info(data)

        rv, data = m.uid('search', None, 'ALL')
        if rv != 'OK':
            sys.exit(1)
        logging.info(data)

        ''' busco mail por mail y lo listo '''
        import re
        unav = re.compile('.*TO:.*(?P<email>\<.*@.*\>).*mailbox unavailable.*', re.I)
        mails = data[0].split()
        for mail in mails:
            rv, data = m.uid('fetch', mail, 'fast')
            size = int(data[0].split()[-1][:-1])
            if size >= (1024 * 1024):
                ''' mas que 1 mega '''
                continue

            rv, data = m.uid('fetch', mail, '(RFC822)')
            logging.info('buscando {}'.format(mail))
            (ui, body) = data[0]
            texto = str(body)
            if unav.match(str(texto)):
                logging.info(texto)
                match = unav.search(str(texto))
                email = match.group('email')
                if email is not None:
                    logging.info(email)
                    #logging.info('\n\n{}\n\n'.format(str(data)))

    finally:
        m.close()
