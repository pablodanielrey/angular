import sys
sys.path.append('../') #definir ruta de acceso al modelo

import psycopg2
import psycopg2.pool


from model import SqlContext
from psycopg2.extras import DictCursor

from model import SqlContext
from model.users.entities.userPassword import UserPassword
from model.users.entities.user import User

from model.designation.entities.designation import Designation
from model.designation.entities.position import Position

h = sys.argv[1]
d = sys.argv[2]
u = sys.argv[3]
p = sys.argv[4]

pool = psycopg2.pool.ThreadedConnectionPool(1, 4, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
ctx = SqlContext(pool)
ctx.getConn()


clazz = Position


orderBy = {"position":True} #separamos para incluirlo en el fetch
ids = clazz.find(ctx, orderBy=orderBy)
for o in ids.fetch(ctx, orderBy=orderBy):
  print(o.__dict__)


ctx.pool.closeall()

"""

#ups = UserPassword.find(ctx, username=['39958407', '39117339'], orderBy={"username":False}).fetch(ctx, orderBy={"username":False})

#buscar designaciones historicas (out=True)
#ids = User.find(ctx)
#for i in designations:
#    print(i.__dict__)


ids = User.find(ctx, dni=["31073351", "27294557"], orderBy={"name":False})

print(ids)

for id in ids:
   print(id)

users = ids.fetch(ctx)
for user in users:
    print(user.__dict__)
"""

ctx.pool.closeall()
