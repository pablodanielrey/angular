import sys
sys.path.append('/home/ivan/www/angular/python') #definir ruta de acceso al modelo

import psycopg2
import psycopg2.pool


from model import SqlContext
from psycopg2.extras import DictCursor


h = sys.argv[1]
d = sys.argv[2]
u = sys.argv[3]
p = sys.argv[4]
 
pool = psycopg2.pool.ThreadedConnectionPool(1, 1, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
con = pool.getconn()
ctx = SqlContext(con)




















