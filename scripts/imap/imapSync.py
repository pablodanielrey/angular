import imaplib
from email.parser import BytesParser
import socket
import sys
import re

pattern_folder = re.compile('\(.*\) \".*\" \"(?P<folder>.*)\"')
pattern_fetch_response = re.compile('.* INTERNALDATE (?P<date>\".*\") RFC822.SIZE (?P<size>\d+)')

def getFolders(imap):
    rv, data = imap.list()
    for d in data:
        match = pattern_folder.match(bytes.decode(d))
        if match:
            yield match.group('folder')

def getMessagesToSync(imap, folder):
    rv, data = imap.select(folder)
    if 'OK' not in rv:
        return
    totalMessages = int(bytes.decode(data[0]))
    print('Buscando mensajes a sincronizar en : {}'.format(folder))
    rv, data = imap.search(None, 'NOT KEYWORD synched')
    nums = data[0].split()
    for n in nums:
        print('Obteniendo mensaje {}'.format(n))
        rv, data = imap.fetch(n, '(FLAGS INTERNALDATE RFC822.SIZE RFC822)')
        match = pattern_fetch_response.match(bytes.decode(data[0][0]))
        yield (n, totalMessages, imaplib.ParseFlags(data[0][0]), match.group('date'), int(match.group('size')), data[0][1])


if __name__ == '__main__':

    guser = sys.argv[1]
    gpass = sys.argv[2]
    euser = sys.argv[3]
    epass = sys.argv[4]

    parser = BytesParser()

    gmail = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        gmail.login(guser, gpass)
        try:
            try:
                ''' creo la carpeta de sincronización dentro de gmail '''
                rv, data = gmail.create('copiados')
                print(rv)
                print(data)
            except Exception as e:
                print(e)

            m = imaplib.IMAP4_SSL('163.10.17.115')
            try:
                m.login(euser, epass)
                try:
                    for folder in getFolders(m):
                        if 'grupos/' in folder:
                            print('Ignorando {}'.format(folder))
                            continue

                        if 'Trash' in folder:
                            print('Ignorando {}'.format(folder))
                            continue

                        for (n, totalMessages, flags, internalDate, size, message) in getMessagesToSync(m, folder):
                            print('Sincronizando mensaje {} {} {} {}'.format(folder, totalMessages, n, size))

                            ''' chequeo que no haya venido de gmail '''
                            headers = parser.parsebytes(message, True)
                            if 'X-Gm-Spam' in headers.keys():
                                m.store(n, '+FLAGS', '(synched)')
                                print('Mensaje {} ya sincronizado'.format(n))
                                continue

                            ''' subo el correo a gmail '''
                            fla = [bytes.decode(x) for x in flags if b'unknown' not in x]
                            try:
                                rv,data = gmail.append('copiados', ' '.join(fla), None, message)
                                if 'OK' in rv:
                                    m.store(n, '+FLAGS', '(synched)')
                                    print(data)

                            except socket.error as v:
                                gmail = imaplib.IMAP4_SSL('imap.gmail.com')
                                gmail.login(guser, gpass)

                            except Exception as e:
                                print(e)

                finally:
                    m.logout()
            finally:
                pass

        finally:
            gmail.logout()
    finally:
        pass
