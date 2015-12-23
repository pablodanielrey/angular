# -*- coding: utf-8 -*-

import uuid, psycopg2, inject, psycopg2.extras
from model.utils import Tools

class Nota:	

    #fields de la tabla
    def _fields(self):
      return """
nota.id AS id, nota.codigo AS codigo, nota.fecha AS fecha, nota.descripcion AS descripcion, nota.observaciones AS observaciones, nota.persona AS persona, 
"""

    #fields de la tabla y sus relaciones
    def _fieldsRelations(self):
      return """
nota.id AS id, nota.codigo AS codigo, nota.fecha AS fecha, nota.descripcion AS descripcion, nota.observaciones AS observaciones, nota.persona AS persona, 
per.id AS per_id, per.nombres AS per_nombres, per.apellidos AS per_apellidos, 
"""

    #fields de la tabla con cadena relaciones
    def _fieldsComplete(self):
      return """
nota.id AS id, nota.codigo AS codigo, nota.fecha AS fecha, nota.descripcion AS descripcion, nota.observaciones AS observaciones, nota.persona AS persona, 
per.id AS per_id, per.nombres AS per_nombres, per.apellidos AS per_apellidos, 
"""


    """
     " concatenar campos principales en un campo alias label
    """
    def _fieldsLabel(self):
      return """CONCAT_WS(', ', nota.codigo) AS label, 
"""

    #definir condicion de busqueda
    def _conditionSearch(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(nota.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(nota.codigo) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(nota.fecha, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(nota.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(nota.observaciones) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(nota.persona AS CHAR) LIKE '%" + search + "%' ) "
      return "(" + condition + ")"

    #definir condicion de busqueda
    def _conditionSearchRelations(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(nota.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(nota.codigo) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(nota.fecha, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(nota.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(nota.observaciones) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(nota.persona AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(per.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(per.nombres) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(per.apellidos) LIKE lower('%" + search + "%')) "
      return "(" + condition + ")"

    #definir condicion de busqueda
    def _conditionSearchComplete(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(nota.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(nota.codigo) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(nota.fecha, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(nota.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(nota.observaciones) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(nota.persona AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(per.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(per.nombres) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(per.apellidos) LIKE lower('%" + search + "%')) "
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
          condition = condition + conn + "(nota.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "codigo": 
          condition = condition + conn + "(lower(nota.codigo) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "descripcion": 
          condition = condition + conn + "(lower(nota.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "observaciones": 
          condition = condition + conn + "(lower(nota.observaciones) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "persona": 
          condition = condition + conn + "(nota.persona = " + search[i+"iv"] + ") "

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
          condition = condition + conn + "(nota.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "codigo": 
          condition = condition + conn + "(lower(nota.codigo) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "descripcion": 
          condition = condition + conn + "(lower(nota.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "observaciones": 
          condition = condition + conn + "(lower(nota.observaciones) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "persona": 
          condition = condition + conn + "(nota.persona = " + search[i+"iv"] + ") "

        if search[i+"if"] == "per_id": 
          condition = condition + conn + "(per.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "per_nombres": 
          condition = condition + conn + "(lower(per.nombres) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "per_apellidos": 
          condition = condition + conn + "(lower(per.apellidos) = lower('" + search[i+"iv"] + "')) "

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
          condition = condition + conn + "(nota.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "codigo": 
          condition = condition + conn + "(lower(nota.codigo) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "descripcion": 
          condition = condition + conn + "(lower(nota.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "observaciones": 
          condition = condition + conn + "(lower(nota.observaciones) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "persona": 
          condition = condition + conn + "(nota.persona = " + search[i+"iv"] + ") "

        if search[i+"if"] == "per_id": 
          condition = condition + conn + "(per.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "per_nombres": 
          condition = condition + conn + "(lower(per.nombres) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "per_apellidos": 
          condition = condition + conn + "(lower(per.apellidos) = lower('" + search[i+"iv"] + "')) "

      return "(" + condition + ")"

    #fields de la tabla con cadena relaciones
    def _leftJoinsComplete(self):
      return """
LEFT OUTER JOIN expedientes.persona AS per ON (nota.persona = per.id)
      """


    def orderByField(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'codigo': 
            return 'codigo ' + value
        if field == 'fecha': 
            return 'fecha ' + value
        if field == 'descripcion': 
            return 'descripcion ' + value
        if field == 'observaciones': 
            return 'observaciones ' + value
        if field == 'persona': 
            return 'persona ' + value

    def orderByFieldRelations(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'codigo': 
            return 'codigo ' + value
        if field == 'fecha': 
            return 'fecha ' + value
        if field == 'descripcion': 
            return 'descripcion ' + value
        if field == 'observaciones': 
            return 'observaciones ' + value
        if field == 'persona': 
            return 'persona ' + value
        if field == 'per_id': 
            return 'per_id ' + value
        if field == 'per_nombres': 
            return 'per_nombres ' + value
        if field == 'per_apellidos': 
            return 'per_apellidos ' + value

    def orderByFieldComplete(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'codigo': 
            return 'codigo ' + value
        if field == 'fecha': 
            return 'fecha ' + value
        if field == 'descripcion': 
            return 'descripcion ' + value
        if field == 'observaciones': 
            return 'observaciones ' + value
        if field == 'persona': 
            return 'persona ' + value
        if field == 'per_id': 
            return 'per_id ' + value
        if field == 'per_nombres': 
            return 'per_nombres ' + value
        if field == 'per_apellidos': 
            return 'per_apellidos ' + value

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
        sql = sql + "	FROM expedientes.nota AS nota"
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
        sql = sql + "	FROM expedientes.nota AS nota"
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

        sql = "SELECT count(DISTINCT nota.id) AS num_rows"
        sql = sql + "	FROM expedientes.nota AS nota"
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

