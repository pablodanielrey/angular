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

def getFolders(imap):
    rv, data = imap.list()
    logging.info(data)
    for d in data:
        logging.info(d)
        match = pattern_folder.match(bytes.decode(d))
        logging.info(match)
        if match:
            logging.info('carpeta reconocida')
            yield match.group('folder')
        else:
            match = pattern2_folder.match(bytes.decode(d))
            logging.info(match)
            if match:
                logging.info('carpeta reconocida')
                yield match.group('folder')
            else:
                logging.info('carpeta no reconocida')

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

    guser = sys.argv[1]
    gpass = sys.argv[2]
    euser = sys.argv[3]
    epass = sys.argv[4]

    logFile = '/var/log/imap-sync-{}-{}.log'.format(guser,str(datetime.datetime.now()))
    logging.basicConfig(filename=logFile, filemode='w', level=logging.DEBUG)
    print('logueando info del proceso sobre : {}'.format(logFile))

    imaplib._MAXLINE = 99999999

    parser = BytesParser()

    logging.info('Conectandose a gmail')
    gmail = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        logging.info('Logueandose en gmail')
        gmail.login(guser, gpass)
        try:
            try:
                ''' creo la carpeta de sincronización dentro de gmail '''
                rv, data = gmail.create('copiados')
                logging.info(rv)
                logging.info(data)
            except Exception as e:
                logging.info(e)

            logging.info('Contectandose a econo')
            m = imaplib.IMAP4('163.10.17.115')
            try:
                logging.info('logueandose a econo')
                m.login(euser, epass)
                try:
                    folders = list(getFolders(m))
                    folders.append('INBOX')
                    for folder in folders:
                        logging.info(folder)
                        if 'grupos/' in folder:
                            logging.info('Ignorando {}'.format(folder))
                            continue

                        if 'Trash' in folder or 'Papelera' in folder:
                            logging.info('Ignorando {}'.format(folder))
                            continue

                        count = 0
                        totalSeconds = 0
                        time1 = datetime.datetime.now()

                        logging.info('Obteniendo mensajes de {}'.format(folder))
                        for data in getMessagesToSync(m, folder):
                            try:
                                if data is None:
                                    continue

                                gfolder = 'copiados/' + folder
                                gfolder = gfolder.replace(' ','')
                                logging.info('Subiendo a ' + gfolder)
                                rrv, ddata = gmail.create(gfolder)
                                if rrv == 'OK':
                                    logging.info('Carpeta creada correctamente')

                                (n, totalMessages, flags, internalDate, size, message) = data
                                time2 = datetime.datetime.now()
                                seconds = (time2 - time1).seconds
                                time1 = time2

                                ''' calculo el tiempo restante en promedio '''
                                count = count + 1
                                totalSeconds = totalSeconds + seconds
                                average = count / totalSeconds if totalSeconds > 0 else 0
                                remainingMessages = totalMessages - count
                                remainingHours = int((remainingMessages * average) // 60)
                                remainingMinutes = int((remainingMessages * average) % 60)

                                logging.info('')
                                logging.info('Mensajes totales :            {}'.format(totalMessages))
                                logging.info('Mensaje actual :              {}'.format(bytes.decode(n)))
                                logging.info('Mensajes restantes :          {}'.format(remainingMessages))
                                logging.info('Tamaño de mensaje :           {}'.format(size))
                                logging.info('Tiempo promedio por mensaje : {}'.format(average))
                                logging.info('Timepo restante :             {:0>2d}:{:0>2d}'.format(remainingHours, remainingMinutes))

                                ''' chequeo que no haya venido de gmail '''
                                headers = parser.parsebytes(message, True)
                                if 'X-Gm-Spam' in headers.keys():
                                    m.store(n, '+FLAGS', '(synched2)')
                                    logging.info('Mensaje {} ya sincronizado'.format(n))
                                    continue

                                ''' subo el correo a gmail '''
                                fla = [bytes.decode(x) for x in flags if b'unknown' not in x]
                                try:

                                    rv,data = gmail.append(gfolder, ' '.join(fla), None, message)
                                    if 'OK' in rv:
                                        m.store(n, '+FLAGS', '(synched2)')
                                        logging.info(data)
                                    else:
                                        logging.info(rv)
                                        logging.info(data)

                                except socket.error as v:
                                    gmail = imaplib.IMAP4_SSL('imap.gmail.com')
                                    gmail.login(guser, gpass)

                                except Exception as e:
                                    logging.info(e)

                            except Exception as e:
                                logging.info(e)

                finally:
                    m.logout()
            finally:
                pass

        finally:
            gmail.logout()
    finally:
        pass
