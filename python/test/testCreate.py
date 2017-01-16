import sys
sys.path.append('../') #definir ruta de acceso al modelo

import psycopg2
import psycopg2.pool


from model import SqlContext
from psycopg2.extras import DictCursor

from model.offices.dao.officeSqlDAO import OfficeSqlDAO



#from model.designation.entities.designation import Designation
#from model.designation.entities.position import Position

h = sys.argv[1]
d = sys.argv[2]
u = sys.argv[3]
p = sys.argv[4]

pool = psycopg2.pool.ThreadedConnectionPool(1,1, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
ctx = SqlContext(pool)
ctx.getConn()

OfficeSqlDAO._createSchema(ctx)


ctx.con.commit()

ctx.pool.closeall()
