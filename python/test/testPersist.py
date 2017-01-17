import sys
sys.path.append('../') #definir ruta de acceso al modelo

import psycopg2
import psycopg2.pool


from model import SqlContext
from psycopg2.extras import DictCursor

from model.sileg.entities.teachingPlace import TeachingPlace
from model.sileg.entities.teachingPosition import TeachingPosition
from model.sileg.entities.teachingDesignation import TeachingDesignation
from model.users.entities.user import User


h = sys.argv[1]
d = sys.argv[2]
u = sys.argv[3]
p = sys.argv[4]

pool = psycopg2.pool.ThreadedConnectionPool(1,1, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
ctx = SqlContext(pool)
ctx.getConn()




d = TeachingDesignation()
d.resolution = "1/07"
d.record = "11/07"
d.placeId = "986d7028-6914-4051-af23-ba37999e3caa"
d.positionId = 'c734729f-d535-4082-9270-a1035c06890b'
d.userId = "9ef4a648-3039-4823-a18b-bc4a223813a4"
d.type = "original"
d.persist(ctx)

"""
u = User()
u.dni = '31073351'
u.name = 'Juan'
u.lastname = 'Pérez'
u.gender = 'Masculino'
u.persist(ctx)


p = TeachingPosition()
p.id = "c734729f-d535-4082-9270-a1035c06890b"
p.position = "Titular"
p.detail = "complejo"
p.persist(ctx)


p = TeachingPlace()
p.name = "Matemática"
p.type = "scatedra"
p.persist(ctx)


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
"""

ctx.con.commit()

ctx.pool.closeall()
