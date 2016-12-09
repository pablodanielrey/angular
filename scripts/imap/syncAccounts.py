import imaplib
import re
import sys


pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')
pattern_validity = re.compile('.* \(UIDVALIDITY (?P<val>\d+)\)')

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
    rv, data = imap.search(None, 'ALL')
    nums = data[0].split()
    for n in nums:
        rv, data = imap.fetch(n, "(FLAGS BODY.PEEK[HEADER.FIELDS (Message-Id)])")
        print(data)
        yield (n, imaplib.ParseFlags(data[0][0]), bytes.decode(data[0][1]).replace('Message-ID:','').strip())

def getMessage(imap, folder, n):
    rv, data = imap.select(folder)
    rv, data = imap.fetch(n, '(RFC822)')
    yield data[0][1]

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

    copied = None
    with open('/tmp/copied.txt','r') as f:
        copied = [n.replace('\n','') for n in f]
        print(copied)

    with open('/tmp/copied.txt','a') as f:
        with imaplib.IMAP4_SSL('imap.gmail.com') as gmail:
            gmail.login(guser, gpass)
            rv, data = gmail.list()
            print(rv)
            print(data)
            rv, data = gmail.create('copiados')
            print(rv)
            print(data)


            with imaplib.IMAP4_SSL('163.10.17.115') as m:
                m.login(euser, epass)
                for (n, fl, u) in getMessagesId(m, 'INBOX'):
                    fla = [bytes.decode(x) for x in fl if b'unknown' not in x]
                    print(fla)
                    if u not in copied:
                        for message in getMessage(gmail, 'INBOX', n):
                            print(u)
                            rv,data = gmail.append('copiados', ' '.join(fla), None, message)
                            if rv == 'OK':
                                f.write(u + '\n')
                                print(data)
