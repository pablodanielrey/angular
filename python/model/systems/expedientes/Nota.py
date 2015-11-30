# -*- coding: utf-8 -*-

import uuid, psycopg2, inject

class Nota:	

    #fields de la tabla
    def _fields(self):
      return """
nota.id AS id, nota.codigo AS codigo, nota.fecha AS fecha, nota.descripcion AS descripcion, nota.observaciones AS observaciones, nota.persona AS persona, 
      """

    #fields de la tabla con cadena relaciones
    def _fieldsComplete(self):
      return """
per.id AS per_id, per.nombres AS per_nombres, per.apellidos AS per_apellidos, 
      """

    #fields de la tabla con cadena relaciones
    def _leftJoinsComplete(self):
      return """
LEFT OUTER JOIN expedientes.persona AS per ON (nota.persona = per.id)
      """

    def rowById(self, con, id):
        sql = "SELECT DISTINCT "
        sql = sql + self._fields()
        sql = sql[:-1] #eliminar ultima coma
        sql = sql + "	FROM expedientes.nota AS nota"
        sql = sql + " WHERE id = %s;"
        
        cur = con.cursor()
        cur.execute(sql, (id, ))
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()
        
    def gridData(self, con):
        sql = "SELECT "
        sql = sql + self._fields()
        sql = sql + self._fieldsComplete()
        sql = sql[:-1] #eliminar ultima coma
        sql = sql + "	FROM expedientes.nota AS nota"
        sql = sql + self._leftJoinsComplete()

        
        cur = con.cursor()
        cur.execute(sql)
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()

