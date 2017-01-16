import sys
sys.path.append('../') #definir ruta de acceso al modelo

import psycopg2
import psycopg2.pool


from model import SqlContext
from psycopg2.extras import DictCursor

from model import SqlContext
from model.users.entities.userPassword import UserPassword
from model.users.entities.user import User
from model.users.entities.mail import Mail
from model.offices.entities.office import Office
from model.laboralinsertion.entities.company import Company
from model.laboralinsertion.entities.contact import Contact


#from model.designation.entities.designation import Designation
#from model.designation.entities.position import Position

h = sys.argv[1]
d = sys.argv[2]
u = sys.argv[3]
p = sys.argv[4]

pool = psycopg2.pool.ThreadedConnectionPool(1, 4, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
ctx = SqlContext(pool)
ctx.getConn()

offices = Office.find(ctx).fetch(ctx, orderBy={"parent":False})

for o in offices:
    print(o.__dict__)

"""
users = User.find(ctx, dni=["31073351"]).fetch(ctx)
for u in users:
    offices = Office.findByUserId(ctx, u.id, email=["soporte@econo.unlp.edu.ar"]).fetch(ctx)
    for o in offices:
        print(o.__dict__)
"""




ctx.pool.closeall()
