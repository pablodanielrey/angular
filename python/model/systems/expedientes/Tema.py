# -*- coding: utf-8 -*-

import uuid, psycopg2, inject
from model.utils import Tools

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

    #definir condicion de busqueda
    def _conditionSearch(self, search = None, alias = "tema"):
      if not search:
        return ''

      condition = ''
      #definir condiciones de id
      condition = condition + "(CAST(" + alias + ".id AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de descripcion
      condition = condition + " OR "
      condition = condition + "(lower(" + alias + ".descripcion) LIKE lower('%" + search + "%')) "
      return "(" + condition + ")"

    #fields de la tabla con cadena relaciones
    def _leftJoinsComplete(self):
      return """
      """

    def rowById(self, con, id):
        sql = "SELECT DISTINCT "
        sql = sql + self._fields()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.tema AS tema"
        sql = sql + " WHERE id = %s;"
        
        cur = con.cursor()
        cur.execute(sql, (id, ))
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()
        
    def gridData(self, con, search = None, pageNumber = 1, pageSize = 40):
        sql = "SELECT "
        sql = sql + self._fields()
        sql = sql + self._fieldsComplete()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.tema AS tema"
        sql = sql + self._leftJoinsComplete()
        cond = self._conditionSearch(search)
        sql = sql + Tools.concat(cond, 'WHERE')
        if pageSize: 
          sql = sql + " LIMIT " + str(pageSize) + " OFFSET " + str((pageNumber - 1) * pageSize) + "; ";
        
        cur = con.cursor()
        cur.execute(sql)
        
        data = []
        for c in cur:
            data.append(c)
        return data

    def numRows(self, con, search = None):
        sql = "SELECT count(DISTINCT tema.id) AS num_rows"
        sql = sql + "	FROM expedientes.tema AS tema"
        sql = sql + self._leftJoinsComplete()
        cond = self._conditionSearch(search)
        sql = sql + Tools.concat(cond, 'WHERE')

        cur = con.cursor()
        cur.execute(sql)
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()[0]

