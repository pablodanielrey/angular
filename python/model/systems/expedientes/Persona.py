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

    """
     " definir condicion de busqueda avanzada
     " @param search Diccionario con los fields a buscar
     " @param connect Conexion
     " @param alias Alias de la tabla
     " @param fieldAlias Alias para identificar a los fields
    """
    def _conditionAdvancedSearch(self, connect, search = None, alias = "pers", fieldAlias = ""):
      if not search or "ic" not in search or int(float(search["ic"])) == 0:
        return ''

      condition = ''
      
      for i in range(0, int(float(search["ic"]))):
        i = str(i)
        #definir condiciones de id
        if search[i+"if"] == fieldAlias + "id": 
          condition = condition + "(" + alias + ".id = " + search[i+"iv"] + ") "

        #definir condiciones de nombres
        if search[i+"if"] == fieldAlias + "nombres": 
          if condition: 
            condition = condition + " " + connect + " "
          condition = condition + "(lower(" + alias + ".nombres) = lower('" + search[i+"iv"] + "')) "
        #definir condiciones de apellidos
        if search[i+"if"] == fieldAlias + "apellidos": 
          if condition: 
            condition = condition + " " + connect + " "
          condition = condition + "(lower(" + alias + ".apellidos) = lower('" + search[i+"iv"] + "')) "
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
        
    def gridData(self, con, filterParams = None):
        search = filterParams["s"] if filterParams and "s" in filterParams else None
        pageNumber = filterParams["p"] if filterParams and "p" in filterParams else 1
        pageSize = filterParams["q"] if filterParams and "q" in filterParams else 40

        sql = "SELECT "
        sql = sql + self._fields()
        sql = sql + self._fieldsComplete()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.persona AS pers"
        sql = sql + self._leftJoinsComplete()
        cond = self._conditionSearch(search)
        sql = sql + Tools.concat(cond, 'WHERE')
        cond2 = self._conditionAdvancedSearch('AND', filterParams)
        sql = sql + Tools.concat(cond2, 'AND', 'WHERE', cond)
        
        if pageSize: 
          sql = sql + " LIMIT " + str(pageSize) + " OFFSET " + str((pageNumber - 1) * pageSize) + "; ";
        
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql)
        
        rows = cur.fetchall()
        data = []
        for row in rows:
            data.append(dict(row))
            
        return data

    def numRows(self, con, filterParams = None):
        search = filterParams["s"] if filterParams and "s" in filterParams else None

        sql = "SELECT count(DISTINCT pers.id) AS num_rows"
        sql = sql + "	FROM expedientes.persona AS pers"
        sql = sql + self._leftJoinsComplete()
        cond = self._conditionSearch(search)
        sql = sql + Tools.concat(cond, 'WHERE')
        cond2 = self._conditionAdvancedSearch('AND', filterParams)
        sql = sql + Tools.concat(cond2, 'AND', 'WHERE', cond)
        
        cur = con.cursor()
        
        cur.execute(sql)
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()[0]

