# -*- coding: utf-8 -*-
import sys
sys.path.append('/root/issues/python') #definir ruta de acceso al modelo
import inject
inject.configure()

import logging

from model.registry import Registry
from model.connection import connection

if __name__ == '__main__':
    reg = inject.instance(Registry)
    conn = connection.Connection(reg.getRegistry('sileg'))
    con = conn.get()

    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM sileg.place WHERE dependence IS NULL;")
        
        for r in cur:      
            cur.execute("""
                    INSERT INTO offices.office (id, name, dend, dout, description, resolution, record, user_id, position_id, place_id, replace_id, original_id, old_id, old_type, old_resolution_out, old_record_out)
                    VALUES (%(id)s, %(start)s, %(end)s, %(out)s, %(description)s, %(resolution)s, %(record)s, %(userId)s, %(positionId)s, %(placeId)s, %(replaceId)s, %(originalId)s, %(oldId)s, %(oldType)s, %(oldResolutionOut)s, %(oldRecordOut)s);
                """, data)
  
    finally:
        conn.put(con)
