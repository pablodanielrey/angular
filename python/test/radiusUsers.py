
import json
import datetime
import pytz
from dateutil.tz import tzlocal
import dateutil
import sys
sys.path.append('../../python')

import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection.connection import Connection
from model.offices.offices import Office
from model.users.users import User, UserPassword


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    import re
    r = re.compile('[a-zA-Z\d]+')

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        userIds = User.findAll(con)
        users = []
        for uid in [i for (i, v) in userIds]:
            users.extend(UserPassword.findByUserId(con, uid))

        with open('/tmp/radius-users', 'w') as f:
            for up in users:
                if r.match(up.username) is None or ' ' in up.username:
                    continue

                f.write("""

{} Cleartext-Password := "{}"
    Service-Type = Framed-User,
    Framed-Protocol = PPP,
    Framed-Compression = Van-Jacobsen-TCP-IP
                """.format(up.username, up.password))

    finally:
        conn.put(con)
