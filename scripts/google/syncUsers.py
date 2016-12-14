from gauth import GAuth

#https://www.googleapis.com/auth/admin.directory.user, https://www.googleapis.com/auth/admin.directory.user.alias, https://mail.google.com/, https://www.googleapis.com/auth/drive, https://www.googleapis.com/auth/spreadsheets


SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.user',
    'https://www.googleapis.com/auth/admin.directory.user.alias',
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
    ]

if __name__ == '__main__':
    service = GAuth.getService('admin', 'directory_v1', SCOPES, 'econo@econo.unlp.edu.ar')

    results = service.users().list(domain='econo.unlp.edu.ar').execute()
    print(results)
    for u in results.get('users', []):
        print(u)
        print('\n\n\n')
