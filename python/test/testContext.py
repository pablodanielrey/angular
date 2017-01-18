import sys
sys.path.append('../') #definir ruta de acceso al modelo

import psycopg2
import psycopg2.pool


from model import SqlContext
from psycopg2.extras import DictCursor

from model.sileg.silegModel import SilegModel




#from model.designation.entities.designation import Designation
#from model.designation.entities.position import Position

h = sys.argv[1]
d = sys.argv[2]
u = sys.argv[3]
p = sys.argv[4]

pool = psycopg2.pool.ThreadedConnectionPool(1, 4, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
ctx = SqlContext(pool)
ctx.getConn()

place = SilegModel.findPositionsActiveByPlace(ctx, "986d7028-6914-4051-af23-ba37999e3caa")


for k in place:
    print(place[k]["position"].__dict__)
    for d in place[k]["designations"]:
        print (d.__dict__)
        print (d.user.__dict__)







ctx.pool.closeall()
