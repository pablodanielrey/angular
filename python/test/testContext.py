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


h = sys.argv[1]
d = sys.argv[2]
u = sys.argv[3]
p = sys.argv[4]

pool = psycopg2.pool.ThreadedConnectionPool(1, 4, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
ctx = SqlContext(pool)
ctx.getConn()


#buscar designaciones historicas (out=True)
ups = UserPassword.find(ctx, username=['39958407', '39117339'], orderBy={"username":False}).fetch(ctx, orderBy={"username":False})
designations = Designation.find(ctx, userId=["d224eaa5-4b15-40bb-9d22-319f78808bca"], out=True)
"""
for up in ups:
    print(up.__dict__)

ctx.pool.closeall()




ids = User.find(ctx, dni=["31073351", "27294557"], orderBy={"name":False})

print(ids)

for id in ids:
   print(id)

users = ids.fetch(ctx)
for user in users:
    print(user.__dict__)


ctx.pool.closeall()
"""
