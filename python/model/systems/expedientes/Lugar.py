# -*- coding: utf-8 -*-

import uuid, psycopg2, inject

class Lugar:	

    #fields de la tabla
    def _fields(self):
      return """
luga.id AS id, luga.descripcion AS descripcion, 
      """

    #fields de la tabla con cadena relaciones
    def _fieldsComplete(self):
      return """
      """

    #fields de la tabla con cadena relaciones
    def _leftJoinsComplete(self):
      return """
      """

    def rowById(self, con, id):
        sql = "SELECT DISTINCT "
        sql = sql + self._fields()
        sql = sql[:-1] #eliminar ultima coma
        sql = sql + "	FROM expedientes.lugar AS luga"
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
        sql = sql + "	FROM expedientes.lugar AS luga"
        sql = sql + self._leftJoinsComplete()

        
        cur = con.cursor()
        cur.execute(sql)
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()

