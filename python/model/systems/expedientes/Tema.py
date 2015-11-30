# -*- coding: utf-8 -*-

import uuid, psycopg2, inject

class Tema:	

    #fields de la tabla
    def _fields(self):
      return """
tema.id AS id, tema.descripcion AS descripcion, 
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
        sql = sql + "	FROM expedientes.tema AS tema"
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
        sql = sql + "	FROM expedientes.tema AS tema"
        sql = sql + self._leftJoinsComplete()

        
        cur = con.cursor()
        cur.execute(sql)
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()

