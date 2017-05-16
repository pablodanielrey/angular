import imaplib
from email.parser import BytesParser
import socket
import sys
import re
import datetime
import logging

#def parse_mailbox(data):
#    flags, b, c = data.partition(' ')
#    separator, b, name = c.partition(' ')
#    return (flags, separator.replace('"', ''), name.replace('"', ''))

def parse_mailbox(data):
    ms = data.split(")")[-1].split("\"")
    if ms[-1] == '':
        return ms[-2].lstrip().rstrip()
    else:
        return ms[-1].lstrip().rstrip()



def getFolders(imap):
    rv, data = imap.list()
    logging.info(data)
    for d in data:
        flags, separator, name = parse_mailbox(bytes.decode(d))
        logging.info(name)
        yield name
    yield 'INBOX'


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)
    euser = sys.argv[1]
    epass = sys.argv[2]

    #logFile = '/var/log/imap-sync-{}-{}.log'.format(guser,str(datetime.datetime.now()))
    #logging.basicConfig(filename=logFile, filemode='w', level=logging.DEBUG)
    #print('logueando info del proceso sobre : {}'.format(logFile))

    imaplib._MAXLINE = 99999999

    parser = BytesParser()

    logging.info('Contectandose a econo')
    m = imaplib.IMAP4('163.10.17.115')
    try:
        logging.info('logueandose a econo')
        m.login(euser, epass)
        try:
            for folder in getFolders(m):
                logging.info(folder)
                if 'grupos/' in folder:
                    logging.info('Ignorando {}'.format(folder))
                    continue

                if 'Trash' in folder or 'Papelera' in folder:
                    logging.info('Ignorando {}'.format(folder))
                    continue
        finally:
            m.logout()
    finally:
        pass
