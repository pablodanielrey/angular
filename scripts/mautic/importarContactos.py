
import MySQLdb
import datetime

db = MySQLdb.connect(host='', user='', passwd='', db='')
try:
    cur = db.cursor()
    try:
        count = 0
        emails = set()

        cur.execute('select email from leads where email is not null')
        for c in cur:
            emails.add(str.lower(c[0]).strip())

        with open('/tmp/cuentas-fce','r') as f:
            for l in f:
                email = l.strip()
                if '@' in email:
                    if email not in emails:
                        print(count)
                        count = count + 1
                        cur.execute('insert into leads (is_published, date_added, created_by, created_by_user, date_modified, modified_by, modified_by_user, email, points) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                     (1, datetime.datetime.now(), 1, "DiTeSi DiTeSi", datetime.datetime.now(), 1, "DiTeSi DiTeSi", email, 0))
                        db.commit()
        print(count)

    finally:
        cur.close()
finally:
    #db.commit()
    db.close()
