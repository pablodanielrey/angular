import imaplib
from email.parser import BytesParser
import socket
import re
import sys
import os


pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')
pattern_validity = re.compile('.* \(UIDVALIDITY (?P<val>\d+)\)')
pattern_folder = re.compile('\(.*\) \".*\" \"(?P<folder>.*)\"')

def getFolders(imap):
    rv, data = imap.list()
    for d in data:
        match = pattern_folder.match(bytes.decode(d))
        if match:
            yield match.group('folder')

def getUidValidity(imap, folder):
    rv, data = imap.status(folder, '(UIDVALIDITY)')
    validity = bytes.decode(data[0])
    print(validity)
    match = pattern_validity.match(validity)
    if not match:
        return None
    valNumber = match.group('val')
    return valNumber

def getUids(imap, folder):
    ''' Obtiene los ids de los correos dentro de una carpeta especifica '''
    validity = getUidValidity(imap, folder)
    rv, data = imap.select(folder)
    rv, data = imap.search(None, 'ALL')
    nums = data[0].split()
    for n in nums:
        rv, data = imap.fetch(n, '(UID)')
        duid = bytes.decode(data[0])
        match = pattern_uid.match(duid)
        if match:
            uid = match.group('uid')
            if uid:
                yield validity + uid

def getMessagesId(imap, folder):
    rv, data = imap.select(folder)
    if rv == 'OK':
        totalMessages = int(bytes.decode(data[0]))
        rv, data = imap.search(None, 'NOT KEYWORD synched')
        nums = data[0].split()
        for n in nums:
            rv, data = imap.fetch(n, "(FLAGS BODY.PEEK[HEADER.FIELDS (Message-Id)])")
            yield (n, totalMessages, imaplib.ParseFlags(data[0][0]), bytes.decode(data[0][1]).replace('Message-ID:','').strip())

def getMessage(imap, folder, n):
    rv, data = imap.select(folder)
    rv, data = imap.fetch(n, '(RFC822)')
    return data[0][1]

def getFlags(imap, folder):
    ''' Obtiene los ids de los correos dentro de una carpeta especifica '''
    rv, data = m.select(folder)
    rv, data = m.search(None, 'ALL')
    nums = data[0].split()
    for n in nums:
        rv, data = imap.fetch(n, '(FLAGS)')
        print(n)
        print(data)
        print(imaplib.ParseFlags(data[0]))
        yield imaplib.ParseFlags(data[0])

def getLabels(imap, folder):
    ''' Obtiene los ids de los correos dentro de una carpeta especifica '''
    rv, data = m.select(folder)
    rv, data = m.search(None, 'ALL')
    nums = data[0].split()
    for n in nums:
        rv, data = imap.fetch(n, '(X-GM-LABELS)')
        print(n)
        print(data)
        yield bytes.decode(data[0])

def getWithFlag(imap, folder, flag):
    rv, data = m.select(folder)
    rv, data = m.search(None, '(KEYWORD {})'.format(flag))
    print(rv)
    print(data)
    nums = data[0].split()
    return nums


if __name__ == '__main__':

    guser = sys.argv[1]
    gpass = sys.argv[2]
    euser = sys.argv[3]
    epass = sys.argv[4]

    home = os.path.expanduser('~')
    configFolder = home + '/.imapSync'
    try:
        os.mkdir(configFolder)
    except Exception as e:
        pass

    foldersLog = configFolder + '/folders.log'
    copiedLog = configFolder + '/copied.log'
    errorsLog = configFolder + '/errors.log'

    ''' cargo la info de los mails ya procesados '''
    copied = []
    try:
        with open(copiedLog,'r') as f:
            copied = [n.replace('\n','') for n in f]
    except Exception as e:
        pass

    try:
        with open(errorsLog,'r') as f:
            copied.extend([n.replace('\n','') for n in f])
    except Exception as e:
        pass

    foldersProcessed = []
    try:
        with open(foldersLog,'r') as f:
            foldersProcessed = [n.replace('\n','') for n in f]
    except Exception as e:
        pass
    foldersProcessed.append('Trash')
    foldersProcessed.append('Papelera')


    parser = BytesParser()
    with open(copiedLog,'a') as f, open(errorsLog, 'a') as err, open(foldersLog, 'a') as fold:
        gmail = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            gmail.login(guser, gpass)
            try:
                try:
                    rv, data = gmail.create('copiados')
                    print(rv)
                    print(data)
                except Exception as e:
                    print(e)

                imaplib.IMAP4.debug = 10
                m = imaplib.IMAP4('163.10.17.115')
                try:
                    m.login(euser, epass)
                    try:
                        rv, data = m.select('INBOX')
                        for folder in getFolders(m):
                            if folder in foldersProcessed:
                                continue

                            if 'grupos' in folder:
                                print('Ignorando carpeta {}'.format(folder))
                                continue

                            print('Seleccionando carpeta {}'.format(folder))
                            for (n, total, fl, u) in getMessagesId(m, folder):
                                fla = [bytes.decode(x) for x in fl if b'unknown' not in x]
                                print('{} {} {} {}'.format(n, total, folder, u))
                                if u in copied:
                                    #m.store(n, '+FLAGS', '(synched)')
                                    pass
                                else:
                                    message = getMessage(m, folder, n)
                                    headers = parser.parsebytes(message, True)
                                    if 'X-Gm-Spam' in headers.keys():
                                        #m.store(n, '+FLAGS', '(synched)')
                                        f.write(u + '\n')
                                        print(u)
                                    else:
                                        print(u)
                                        try:
                                            rrv, ddata = gmail.select('copiados/'+folder)
                                            if rrv != 'OK':
                                                rrv, ddata = gmail.create('copiados/'+folder)
                                                if rrv == 'OK':
                                                    print('Creando carpeta {} ok'.format('copiados/'+folder))
                                            rv,data = gmail.append('copiados/'+folder, ' '.join(fla), None, message)
                                            print(rv)
                                            if rv == 'OK':
                                                f.write(u + '\n')
                                                #m.store(n, '+FLAGS', '(synched)')
                                                print(data)

                                        except socket.error as v:
                                            gmail = imaplib.IMAP4_SSL('imap.gmail.com')
                                            gmail.login(guser, gpass)

                                        except Exception as e:
                                            err.write(u + '\n')
                                            print(e)

                            fold.write(folder + '\n')

                    finally:
                        m.logout()
                finally:
                    #m.close()
                    pass

            finally:
                gmail.logout()
        finally:
            #gmail.close()
            pass
