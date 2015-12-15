# -*- coding: utf-8 -*-

import uuid, psycopg2, inject, psycopg2.extras
from model.utils import Tools

class Persona:	

    #fields de la tabla
    def _fields(self):
      return """
pers.id AS id, pers.nombres AS nombres, pers.apellidos AS apellidos, 
      """

    #fields de la tabla con cadena relaciones
    def _fieldsComplete(self):
      return """
      """

    #definir condicion de busqueda
    def _conditionSearch(self, search = None, alias = "pers"):
      if not search:
        return ''

      condition = ''
      #definir condiciones de id
      condition = condition + "(CAST(" + alias + ".id AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de nombres
      condition = condition + " OR "
      condition = condition + "(lower(" + alias + ".nombres) LIKE lower('%" + search + "%')) "
      #definir condiciones de apellidos
      condition = condition + " OR "
      condition = condition + "(lower(" + alias + ".apellidos) LIKE lower('%" + search + "%')) "
      return "(" + condition + ")"

    #fields de la tabla con cadena relaciones
    def _leftJoinsComplete(self):
      return """
      """

    def rowById(self, con, id):
        sql = "SELECT DISTINCT "
        sql = sql + self._fields()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.persona AS pers"
        sql = sql + " WHERE id = %s;"
        
        cur = con.cursor()
        cur.execute(sql, (id, ))
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()
        
    def gridData(self, con, filterParams):
        search = None
        pageNumber = filterParams["p"] if filterParams["p"] else 1
        pageSize = filterParams["q"] if filterParams["q"] else 40
        sql = "SELECT "
        sql = sql + self._fields()
        sql = sql + self._fieldsComplete()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.persona AS pers"
        sql = sql + self._leftJoinsComplete()
        cond = self._conditionSearch(search)
        sql = sql + Tools.concat(cond, 'WHERE')
        if pageSize: 
          sql = sql + " LIMIT " + str(pageSize) + " OFFSET " + str((pageNumber - 1) * pageSize) + "; ";
        
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql)
        
        rows = cur.fetchall()
        data = []
        for row in rows:
            data.append(dict(row))
            
        return data

    def numRows(self, con, search = None):
        sql = "SELECT count(DISTINCT pers.id) AS num_rows"
        sql = sql + "	FROM expedientes.persona AS pers"
        sql = sql + self._leftJoinsComplete()
        cond = self._conditionSearch(search)
        sql = sql + Tools.concat(cond, 'WHERE')

        cur = con.cursor()
        cur.execute(sql)
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()[0]

