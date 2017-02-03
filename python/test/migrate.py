import sys
sys.path.append('../') #definir ruta de acceso al modelo

import psycopg2
import psycopg2.pool



from model import SqlContext
from psycopg2.extras import DictCursor

from model.offices.dao.officeSqlDAO import OfficeSqlDAO
from model.sileg.dao.teachingDesignationSqlDAO import TeachingDesignationSqlDAO






"""
antes de todo ejecutar:

INERT INTO designations.position (id, position, type, created) VALUES ('1', 'Cumple Funcion', 0, now());
"""














h = sys.argv[1]
d = sys.argv[2]
u = sys.argv[3]
p = sys.argv[4]

pool = psycopg2.pool.ThreadedConnectionPool(1,1, host=h, database=d, user=u, password=p, cursor_factory=DictCursor)
ctx = SqlContext(pool)
ctx.getConn()







def insertPlace(p):
    cur = ctx.con.cursor()
    print("insert place " + p["id"])
    try:
        cur.execute("""
            INSERT INTO designations.place (id, name, type, removed, public)
            VALUES (%(id)s, %(name)s, %(type)s, %(removed)s, %(public)s)
        """, p)


        cur.execute("""
            INSERT INTO offices.office (id, telephone, nro, email, area, assistance)
            VALUES (%(id)s, %(telephone)s, %(nro)s, %(email)s, %(area)s, %(assistance)s)
        """, p)


    finally:
        cur.close()






def insertDesignationsPosition(p):
    cur = ctx.con.cursor()
    print("insert designations.position " + p["id"])
    try:
        cur.execute("""
            INSERT INTO designations.position (id, position, type, created)
            VALUES (%(id)s, %(position)s, %(type)s, %(created)s);
        """, p)



    finally:
        cur.close()





def insertSilegPosition(p):
    cur = ctx.con.cursor()
    print("insert sileg.position_ " + p["id"])
    try:
        insertDesignationsPosition(p)

        cur.execute("""
            INSERT INTO sileg.position_ (id, detail)
            VALUES (%(id)s, %(detail)s);
        """, p)


    finally:
        cur.close()



def insertDesignationsDesignation_(p):
    cur = ctx.con.cursor()
    print("insert designations.designation_ " + p["id"])
    try:
        cur.execute("""
            INSERT INTO designations.designation_ (id, type, dstart, dend, user_id, place_id, position_id, parent_id, start_id, created)
            VALUES (%(id)s, %(type)s, %(dstart)s, %(dend)s, %(user_id)s, %(place_id)s, %(position_id)s, %(parent_id)s, %(start_id)s, %(created)s);
        """, p)

    finally:
        cur.close()

def insertSilegDesignation_(p):
    cur = ctx.con.cursor()

    insertDesignationsDesignation_(p)

    print("insert sileg.designation_ " + p["id"])
    try:
        cur.execute("""
            INSERT INTO sileg.designation_ (id, dout, resolution, record)
            VALUES (%(id)s, %(dout)s, %(resolution)s, %(record)s);
        """, p)

    finally:
        cur.close()


def designationsPlaceIds():
    cur = ctx.con.cursor()

    try:
        cur.execute("""
            SELECT id
            FROM designations.place
        """)
        return [c["id"] for c in cur]

    finally:
        cur.close()


def designationsDesignation_Ids():
    cur = ctx.con.cursor()

    try:
        cur.execute("""
            SELECT id
            FROM designations.designation_
        """)
        return [c["id"] for c in cur]

    finally:
        cur.close()


def designationsPositionIds():
    cur = ctx.con.cursor()

    try:
        cur.execute("""
            SELECT id
            FROM designations.position
        """)
        return [c["id"] for c in cur]

    finally:
        cur.close()



def officesWithoutParent():
    #Migrar offices.offices a offices.place y office.offices migrar inicialmente las oficinas sin padre
    #Actualmente, todo lo que esta en offices.offices se migra a offices.place y offices.offices,
    #  habria que analizar que es lo que corresopnde a offices.offices solo, por ahora se migra todo porque resulta confuso distinguirlas
    cur = ctx.con.cursor()
    try:
        cur.execute("""
            SELECT id, name, telephone, email, parent, area, assistance, type, nro, removed, public
            FROM offices.offices
            WHERE parent IS NULL;
        """)

        designations_place_ids = designationsPlaceIds()

        for c in cur:
            if c["id"] not in designations_place_ids:
                insertPlace(c)

    finally:
        cur.close()







def offices():
    cur = ctx.con.cursor()
    try:
        cur.execute("""
            SELECT id, name, telephone, email, parent, area, assistance, type, nro, removed, public
            FROM offices.offices
        """)

        offices_offices = [c for c in cur]

        designations_place_ids = designationsPlaceIds()

        flag = False

        for o in offices_offices:
            if o["id"] not in designations_place_ids:
                flag = True
                insertPlace(o)

        if flag:
            print("recursion")
            offices()

    finally:
        cur.close()





def silegPosition():
    cur = ctx.con.cursor()
    try:
        cur.execute("""
            SELECT id, position, type, created, detail
            FROM designations.positions
            WHERE detail IS NOT NULL;
        """)

        designations_positions = [c for c in cur]

        designations_position_ids = designationsPositionIds()

        for p in designations_positions:
            if p["id"] not in designations_position_ids:
                insertSilegPosition(p)

    finally:
        cur.close()






def officesDesignations():
    cur = ctx.con.cursor()
    try:
        cur.execute("""
            SELECT id, user_id, office_id AS place_id, sstart AS dstart, send AS dend, '1' as position_id, null as type, null AS parent_id, null AS start_id, now() AS created
            FROM offices.designations;
        """)

        officesDesignations = [c for c in cur]

        ids = designationsDesignation_Ids()

        for p in officesDesignations:
            if p["id"] not in ids:
                insertDesignationsDesignation_(p)

    finally:
        cur.close()






def designationsDesignations():
    cur = ctx.con.cursor()
    try:
        cur.execute("""
            SELECT id, user_id, office_id AS place_id, sstart AS dstart, send AS dend, '1' as position_id, null as type, null AS parent_id, null AS start_id, created AS created
            FROM designations.designations;
        """)

        designationsDesignations = [c for c in cur]

        ids = designationsDesignation_Ids()

        for p in designationsDesignations:
            if p["id"] not in ids:
                insertDesignationsDesignation_(p)

    finally:
        cur.close()


#designations.designation where position_id = 1
def migrar_designations_designation():
    cur = ctx.con.cursor()
    try:
        cur.execute("""
            SELECT id, user_id, office_id AS place_id, dstart, dend, position_id, null as type, null AS parent_id, null AS start_id, created AS created
            FROM designations.designation
            WHERE position_id = '1';
        """)

        designationsDesignations = [c for c in cur]

        ids = designationsDesignation_Ids()

        for p in designationsDesignations:
            if p["id"] not in ids:
                insertDesignationsDesignation_(p)

    finally:
        cur.close()



#designations.designation where position_id = 1
def migrar_designations_designation2():
    cur = ctx.con.cursor()
    try:
        cur.execute("""
            SELECT id, user_id, office_id AS place_id, dstart, dend, dout, description as type, resolution, record, position_id,  parent_id, original_id AS start_id, created
            FROM designations.designation
            WHERE position_id != '1';
        """)

        designationsDesignations = [c for c in cur]

        ids = designationsDesignation_Ids()

        for p in designationsDesignations:
            if p["id"] not in ids:
                insertSilegDesignation_(p)

    finally:
        cur.close()




#officesWithoutParent()
#offices()
#silegPosition()
#officesDesignations()
#designationsDesignations()
#migrar_designations_designation()
migrar_designations_designation2()


ctx.con.commit()
ctx.closeConn()
