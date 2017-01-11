import sys
sys.path.append('/home/ivan/www/angular/python') #definir ruta de acceso al modelo

import psycopg2
import psycopg2.pool


from model import SqlContext
from psycopg2.extras import DictCursor

from model import SqlContext
from model.users.entities.userPassword import UserPassword
from model.users.entities.user import User


h = sys.argv[1]
d = sys.argv[2]
u = sys.argv[3]
p = sys.argv[4]

pool = psycopg2.pool.ThreadedConnectionPool(1, 3, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
ctx = SqlContext(pool)


ids = UserPassword.find(ctx).fetch(ctx)
print(ids)
for id in ids:
    print(id)

ctx.pool.closeall()
"""
pool = psycopg2.pool.ThreadedConnectionPool(1, 2, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
ctx = SqlContext(pool)

users = User.find(ctx).fetch(ctx)
for user in users:
    print(user.__dict__)
    

ctx.pool.closeall()
"""
















