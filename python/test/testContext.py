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


clazz = Contact

orderBy = {} #separamos para incluirlo en el fetch
#orderBy = {"position":True} #separamos para incluirlo en el fetch
ids = clazz.find(ctx)
for o in ids.fetch(ctx, orderBy=orderBy):
  print(o.__dict__)


c = clazz()
c.id = "AAA"
c.delete(ctx)

ctx.pool.closeall()
