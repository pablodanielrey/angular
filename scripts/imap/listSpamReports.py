import imaplib
from email.parser import BytesParser
from email.utils import parseaddr
import sys
import os

if __name__ == '__main__':

    cuser = sys.argv[1]
    cpass = sys.argv[2]

    parser = BytesParser()

    home = os.path.expanduser('~')
    configFolder = home + '/.spamReport'
    try:
        os.mkdir(configFolder)
    except Exception as e:
        pass

    with open(configFolder + '/spam.txt', 'a') as f:
        m = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            m.login(cuser, cpass)
            try:
                rv, data = m.select('INBOX')
                rv, data = m.search(None, 'FROM <staff@hotmail.com>')
                for n in bytes.decode(data[0]).split():
                    print(n)
                    rv, data = m.fetch(n, '(RFC822)')
                    body = data[0][1]
                    e = parser.parsebytes(body)
                    for part in e.walk():
                        if 'message/rfc822' in part.get_content_type():
                            originalMessage = part.get_payload()[0]
                            recip = parseaddr(originalMessage['X-HmXmrOriginalRecipient'])[1]
                            fr = parseaddr(originalMessage['From'])[1]
                            f.write('{} {}\n'.format(recip, fr))

            finally:
                m.logout()
        finally:
            pass
