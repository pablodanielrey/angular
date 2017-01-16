import sys
sys.path.append('../') #definir ruta de acceso al modelo

import psycopg2
import psycopg2.pool


from model import SqlContext
from psycopg2.extras import DictCursor

from model.offices.entities.office import Office

h = sys.argv[1]
d = sys.argv[2]
u = sys.argv[3]
p = sys.argv[4]

pool = psycopg2.pool.ThreadedConnectionPool(1,1, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
ctx = SqlContext(pool)
ctx.getConn()

o = Office();
o.name = "Test Area"
o.number = "1234"
o.type = 'area'
o.persist(ctx);

o2 = Office()
o2.name = "Test Subarea"
o2.number = "6789"
o2.parent = o.id
o2.type = 'area'
o2.persist(ctx);

o2.delete(ctx)

ctx.con.commit()

ctx.pool.closeall()
