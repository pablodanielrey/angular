# -*- coding: utf-8 -*-

import uuid, psycopg2, inject, psycopg2.extras
from model.utils import Tools

class Lugar:	

    #fields de la tabla
    def _fields(self):
      return """
luga.id AS id, luga.descripcion AS descripcion, 
"""

    #fields de la tabla con cadena relaciones
    def _fieldsComplete(self):
      return """
luga.id AS id, luga.descripcion AS descripcion, 
"""


    """
     " concatenar campos principales en un campo alias label
    """
    def _fieldsLabel(self):
      return """CONCAT_WS(', ', luga.descripcion) AS label, 
"""

    #definir condicion de busqueda
    def _conditionSearch(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(luga.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(luga.descripcion) LIKE lower('%" + search + "%')) "
      return "(" + condition + ")"

    #definir condicion de busqueda
    def _conditionSearchRelations(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(luga.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(luga.descripcion) LIKE lower('%" + search + "%')) "
      return "(" + condition + ")"

    #definir condicion de busqueda
    def _conditionSearchComplete(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(luga.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(luga.descripcion) LIKE lower('%" + search + "%')) "
      return "(" + condition + ")"

    """
     " definir condicion de busqueda avanzada
     " @param search Diccionario con los fields a buscar
     " @param connect Conexion
     " @param alias Alias de la tabla
     " @param fieldAlias Alias para identificar a los fields
    """
    def _conditionAdvancedSearch(self, connect, search = None):
      if not search or "ic" not in search or int(float(search["ic"])) == 0:
        return ''

      condition = ''
      
      for i in range(0, int(float(search["ic"]))):
        conn = "" if not condition else connect + " "
        i = str(i)
        if search[i+"if"] == "id": 
          condition = condition + conn + "(luga.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "descripcion": 
          condition = condition + conn + "(lower(luga.descripcion) = lower('" + search[i+"iv"] + "')) "

      return "(" + condition + ")"

    """
     " definir condicion de busqueda avanzada
     " @param search Diccionario con los fields a buscar
     " @param connect Conexion
     " @param alias Alias de la tabla
     " @param fieldAlias Alias para identificar a los fields
    """
    def _conditionAdvancedSearchRelations(self, connect, search = None):
      if not search or "ic" not in search or int(float(search["ic"])) == 0:
        return ''

      condition = ''
      
      for i in range(0, int(float(search["ic"]))):
        conn = "" if not condition else connect + " "
        i = str(i)
        if search[i+"if"] == "id": 
          condition = condition + conn + "(luga.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "descripcion": 
          condition = condition + conn + "(lower(luga.descripcion) = lower('" + search[i+"iv"] + "')) "

      return "(" + condition + ")"

    """
     " definir condicion de busqueda avanzada
     " @param search Diccionario con los fields a buscar
     " @param connect Conexion
     " @param alias Alias de la tabla
     " @param fieldAlias Alias para identificar a los fields
    """
    def _conditionAdvancedSearchComplete(self, connect, search = None):
      if not search or "ic" not in search or int(float(search["ic"])) == 0:
        return ''

      condition = ''
      
      for i in range(0, int(float(search["ic"]))):
        conn = "" if not condition else connect + " "
        i = str(i)
        if search[i+"if"] == "id": 
          condition = condition + conn + "(luga.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "descripcion": 
          condition = condition + conn + "(lower(luga.descripcion) = lower('" + search[i+"iv"] + "')) "

      return "(" + condition + ")"

    #fields de la tabla con cadena relaciones
    def _leftJoinsComplete(self):
      return """
      """


    def orderByField(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'descripcion': 
            return 'descripcion ' + value

    def orderByFieldRelations(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'descripcion': 
            return 'descripcion ' + value

    def orderByFieldComplete(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'descripcion': 
            return 'descripcion ' + value

    def orderBy(self, fields):
        if not fields:
            return ""
        
        sql = ""

        for field in fields:
            for f in field:
                sqlAux = self.orderByField(f, field[f])
                sql = sql + Tools.concat(sqlAux, ', ', 'ORDER BY ', sql)
		
        return sql
        
    def orderByRelations(self, fields):
        if not fields:
            return ""
        
        sql = ""

        for field in fields:
            for f in field:
                sqlAux = self.orderByFieldRelations(f, field[f])
                sql = sql + Tools.concat(sqlAux, ', ', 'ORDER BY ', sql)
		
        return sql
        
    def orderByComplete(self, fields):
        if not fields:
            return ""
        
        sql = ""

        for field in fields:
            for f in field:
                sqlAux = self.orderByFieldComplete(f, field[f])
                sql = sql + Tools.concat(sqlAux, ', ', 'ORDER BY ', sql)
		
        return sql
    def _fieldsExtra(self):
      sql = self._fields()
      sql = sql + self._fieldsLabel()
      sql = sql[:sql.rfind(",")] #eliminar ultima coma

    def _fieldsRelationsExtra(self):
      sql = self._fieldsRelations()
      sql = sql + self._fieldsLabel()
      sql = sql[:sql.rfind(",")] #eliminar ultima coma
    
    def _fieldsCompleteExtra(self):
      sql = self._fieldsComplete()
      sql = sql + self._fieldsLabel()
      sql = sql[:sql.rfind(",")] #eliminar ultima coma
    def rowById(self, con, id):
        sql = "SELECT DISTINCT "
        sql = sql + self._fields()
        sql = sql + self._fieldsLabel()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.lugar AS luga"
        sql = sql + " WHERE id = %s;"
        
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql, (id, ))
        if cur.rowcount <= 0:
            return None
            
        return dict(cur.fetchone())
        
    def gridData(self, con, filterParams = None):
        search = filterParams["s"] if filterParams and "s" in filterParams else None
        pageNumber = filterParams["p"] if filterParams and "p" in filterParams else 1
        pageSize = filterParams["q"] if filterParams and "q" in filterParams else 40
        orderBy = [{filterParams["of"]: filterParams["ot"]}] if "of" in filterParams else []

        sql = "SELECT "
        sql = sql + self._fields()
        sql = sql + self._fieldsComplete()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.lugar AS luga"
        sql = sql + self._leftJoinsComplete()
        cond = self._conditionSearch(search)
        sql = sql + Tools.concat(cond, 'WHERE')
        cond2 = self._conditionAdvancedSearch('AND', filterParams)
        sql = sql + Tools.concat(cond2, 'AND', 'WHERE', cond)
        sql = sql + self.orderByComplete(orderBy)
        
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

        sql = "SELECT count(DISTINCT luga.id) AS num_rows"
        sql = sql + "	FROM expedientes.lugar AS luga"
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

