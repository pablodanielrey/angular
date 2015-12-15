# -*- coding: utf-8 -*-

import uuid, psycopg2, inject, psycopg2.extras
from model.utils import Tools

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

    #definir condicion de busqueda
    def _conditionSearch(self, search = None, alias = "nota"):
      if not search:
        return ''

      condition = ''
      #definir condiciones de id
      condition = condition + "(CAST(" + alias + ".id AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de codigo
      condition = condition + " OR "
      condition = condition + "(lower(" + alias + ".codigo) LIKE lower('%" + search + "%')) "
      #definir condiciones de fecha
      condition = condition + " OR "
      condition = condition + "(CAST(to_char(" + alias + ".fecha, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de descripcion
      condition = condition + " OR "
      condition = condition + "(lower(" + alias + ".descripcion) LIKE lower('%" + search + "%')) "
      #definir condiciones de observaciones
      condition = condition + " OR "
      condition = condition + "(lower(" + alias + ".observaciones) LIKE lower('%" + search + "%')) "
      #definir condiciones de persona
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".persona AS CHAR) LIKE '%" + search + "%' ) "

      return "(" + condition + ")"

    #fields de la tabla con cadena relaciones
    def _leftJoinsComplete(self):
      return """
LEFT OUTER JOIN expedientes.persona AS per ON (nota.persona = per.id)
      """

    def rowById(self, con, id):
        sql = "SELECT DISTINCT "
        sql = sql + self._fields()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.nota AS nota"
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
        sql = sql + "	FROM expedientes.nota AS nota"
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
        sql = "SELECT count(DISTINCT nota.id) AS num_rows"
        sql = sql + "	FROM expedientes.nota AS nota"
        sql = sql + self._leftJoinsComplete()
        cond = self._conditionSearch(search)
        sql = sql + Tools.concat(cond, 'WHERE')

        cur = con.cursor()
        cur.execute(sql)
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()[0]

