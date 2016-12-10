import imaplib
import sys
import re

pattern_folder = re.compile('\(.*\) \".*\" \"(?P<folder>.*)\"')

def getFolders(imap):
    rv, data = imap.list()
    for d in data:
        match = pattern_folder.match(bytes.decode(d))
        if match:
            yield match.group('folder')

if __name__ == '__main__':
        euser = sys.argv[1]
        epass = sys.argv[2]
        m = imaplib.IMAP4_SSL('163.10.17.115')
        try:
            m.login(euser, epass)
            try:
                for folder in getFolders(m):
                    rv, data = m.select(folder, True)
                    if 'OK' in rv:
                        rv, data = m.search(None, 'KEYWORD synched')
                        nums = data[0].split()
                        print('{} : {}'.format(folder, len(nums)))
            finally:
                m.logout()
        finally:
            pass
