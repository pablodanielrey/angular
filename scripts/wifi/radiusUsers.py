
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
from model.offices.office import Office
from model.users.users import User, UserPassword


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    # registro usuarios que son autoridades
    autoridades = [
        '24892148',     # pablo diaz
        '27294557',     # pablo rey
        '30057880',     # charly
        '31993212',     # adrian
        '25952190',     # julieta
        '13908434',     # laura catani
        '18283954',     # armengol
        '26578935',     # masson
        '26250165',     # eduardo degiusti
        '23454309',     # marina gs
        '20294338',     # diego felices
        '17755153',     # leo gasparini
        '22349070',     # mariana marchioni
        '29763750',     # paula beyries
        '30001823',     # walter blanco
        '27821597',     # maxi saucedo
        '31381082',     # emanuel pais
        '31073351',     # ivan castañeda
        '29694757',     # alejandro oporto
        '34928857',     # miguel macagno
        '29728322',     # daniel demaria
        '38866283',     # nicolas cece
        '35487193',      #fernanda bernasconi
        '37809316',      # albana velozo
        '13975264',      # sandra monti
        '33782574',      # adrian garcia
        '31433408',      # ezequiel alustiza
        '34058503',      # Florencia Moscoso
        '34770399',      # Rocio Bogue
        '37809316',      # Albana
        '17082410',     # Estela Molteni
        '28768560'      # Sabrina Tombesi
    ]

    import re
    r = re.compile('[a-zA-Z\d]+')

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        Connection.readOnly(con)
        #userIds = User.findAll(con)
        userss = User.findByType(con, ['teacher'])
        userss.extend(User.findByDni(con, autoridades))
        users = [i for (i,v) in userss]
        usersp = []
        for uid in users:
            usersp.extend(UserPassword.findByUserId(con, uid))

        with open('/tmp/radius-users', 'w') as f:
            for up in usersp:
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
