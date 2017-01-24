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
from model.offices.entities.office import Office



h = sys.argv[1]
d = sys.argv[2]
u = sys.argv[3]
p = sys.argv[4]

pool = psycopg2.pool.ThreadedConnectionPool(1,1, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
ctx = SqlContext(pool)
ctx.getConn()


o = Office();
o.name = "Departamento de prueba"
o.number = "1234"
o.type = 'departamento'
o.persist(ctx);


"""
d = TeachingDesignation()
d.resolution = "1/07"
d.record = "11/07"
d.placeId = "bd6b7d47-d7c6-46a7-bb92-b305dfdd631d"
d.positionId = "d3384566-5e31-4cc3-8291-fd180208ffd1"
d.userId = "d44e92c1-d277-4a45-81dc-a72a76f6ef8d"
d.type = "original"
d.persist(ctx)


p = TeachingPlace()
p.name = "Matemática"qwq
p.type = "catedra"
p.persist(ctx)






u = User()
u.dni = '31073351'
u.name = 'Juan'
u.lastname = 'Pérez'
u.gender = 'Masculino'
u.persist(ctx)









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
