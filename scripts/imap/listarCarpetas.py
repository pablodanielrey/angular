import imaplib
from email.parser import BytesParser
import socket
import sys
import re
import datetime
import logging



pattern_folder = re.compile('\(.*?\) \".*?\" \"(?P<folder>.*?)\"')
pattern2_folder = re.compile('\(.*?\) \".*?\" (?P<folder>.*?)')
pattern_size_response = re.compile('.*RFC822.SIZE (?P<size>\d+)')
pattern_fetch_response = re.compile('.* INTERNALDATE (?P<date>\".*\") RFC822.SIZE (?P<size>\d+)')
GMAIL_LIMIT = 25000000

def parse_mailbox(data):
    flags, b, c = data.partition(' ')
    separator, b, name = c.partition(' ')
    return (flags, separator.replace('"', ''), name.replace('"', ''))


def getFolders(imap):
    rv, data = imap.list()
    logging.info(data)
    for d in data:
        flags, separator, name = parse_mailbox(bytes.decode(d))
        logging.info(name)
        yield name
        #match = pattern_folder.match(bytes.decode(d))
        #logging.info(match)
        #if match:
        #   logging.info('carpeta reconocida')
        #    yield match.group('folder')
        #else:
        #    match = pattern2_folder.match(bytes.decode(d))
        #    logging.info(match)
        #    if match:
        #        logging.info('carpeta reconocida')
        #        yield match.group('folder')
        #    else:
        #        logging.info('carpeta no reconocida')
    yield 'INBOX'

def getMessagesToSync(imap, folder):
    try:
        logging.info(folder)
        if ' ' in folder:
            rv, data = imap.select('\"' + folder + '\"')
            if 'OK' not in rv:
                rv, data = imap.select(folder)
                if 'OK' not in rv:
                    logging.info('ERROR selecconando carpeta desde el server imap econo')
                    logging.info(rv)
                    logging.info(data)
                    return
        else:
            rv, data = imap.select(folder)
            if 'OK' not in rv:
                logging.info('ERROR selecconando carpeta desde el server imap econo')
                logging.info(rv)
                logging.info(data)
                return

        #totalMessages = int(bytes.decode(data[0]))
        logging.info('Buscando mensajes a sincronizar en : {}'.format(folder))
        rv, data = imap.search(None, 'NOT KEYWORD synched2')
        #rv, data = imap.search(None,'ALL')
        nums = data[0].split()
        totalMessages = len(nums)
        for n in nums:
            logging.info('Obteniendo mensaje {}'.format(n))

            ''' chequeo el tamaño primero '''
            rv, data = imap.fetch(n, '(RFC822.SIZE)')
            if 'OK' not in rv:
                continue
            match = pattern_size_response.match(bytes.decode(data[0]))
            if not match:
                continue
            size = int(match.group('size'))
            if size >= GMAIL_LIMIT:
                logging.info('Ignorando correo con tamaño : {}'.format(size))
                continue

            rv, data = imap.fetch(n, '(FLAGS INTERNALDATE RFC822.SIZE RFC822)')
            match = pattern_fetch_response.match(bytes.decode(data[0][0]))
            yield (n, totalMessages, imaplib.ParseFlags(data[0][0]), match.group('date'), int(match.group('size')), data[0][1])

    except Exception as e:
        logging.info(e)
        yield None

if __name__ == '__main__':

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
