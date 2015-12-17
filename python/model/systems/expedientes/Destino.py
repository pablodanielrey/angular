# -*- coding: utf-8 -*-

import uuid, psycopg2, inject, psycopg2.extras
from model.utils import Tools

class Destino:	

    #fields de la tabla
    def _fields(self):
      return """
dest.id AS id, dest.fecha_entrada AS fecha_entrada, dest.fecha_salida AS fecha_salida, dest.expediente AS expediente, dest.lugar AS lugar, 
      """

    #fields de la tabla con cadena relaciones
    def _fieldsComplete(self):
      return """
exp.id AS exp_id, exp.numero AS exp_numero, exp.fecha_origen AS exp_fecha_origen, exp.fecha_entrada AS exp_fecha_entrada, exp.archivo_numero AS exp_archivo_numero, exp.archivo_anio AS exp_archivo_anio, exp.antecedente AS exp_antecedente, exp.extracto AS exp_extracto, exp.resolucion_iniciador AS exp_resolucion_iniciador, exp.iniciador AS exp_iniciador, exp.agregado AS exp_agregado, exp.lugar_iniciador AS exp_lugar_iniciador, exp.tema AS exp_tema, exp.ultimo_destino AS exp_ultimo_destino, 
exp_ini.id AS exp_ini_id, exp_ini.nombres AS exp_ini_nombres, exp_ini.apellidos AS exp_ini_apellidos, 
exp_agr.id AS exp_agr_id, exp_agr.numero AS exp_agr_numero, exp_agr.fecha_origen AS exp_agr_fecha_origen, exp_agr.fecha_entrada AS exp_agr_fecha_entrada, exp_agr.archivo_numero AS exp_agr_archivo_numero, exp_agr.archivo_anio AS exp_agr_archivo_anio, exp_agr.antecedente AS exp_agr_antecedente, exp_agr.extracto AS exp_agr_extracto, exp_agr.resolucion_iniciador AS exp_agr_resolucion_iniciador, exp_agr.iniciador AS exp_agr_iniciador, exp_agr.agregado AS exp_agr_agregado, exp_agr.lugar_iniciador AS exp_agr_lugar_iniciador, exp_agr.tema AS exp_agr_tema, exp_agr.ultimo_destino AS exp_agr_ultimo_destino, 
exp_agr_ini.id AS exp_agr_ini_id, exp_agr_ini.nombres AS exp_agr_ini_nombres, exp_agr_ini.apellidos AS exp_agr_ini_apellidos, 
exp_agr_li.id AS exp_agr_li_id, exp_agr_li.descripcion AS exp_agr_li_descripcion, 
exp_agr_tem.id AS exp_agr_tem_id, exp_agr_tem.descripcion AS exp_agr_tem_descripcion, 
exp_li.id AS exp_li_id, exp_li.descripcion AS exp_li_descripcion, 
exp_tem.id AS exp_tem_id, exp_tem.descripcion AS exp_tem_descripcion, 
lug.id AS lug_id, lug.descripcion AS lug_descripcion, 
expeYud.id AS expeYud_id, expeYud.numero AS expeYud_numero, expeYud.fecha_origen AS expeYud_fecha_origen, expeYud.fecha_entrada AS expeYud_fecha_entrada, expeYud.archivo_numero AS expeYud_archivo_numero, expeYud.archivo_anio AS expeYud_archivo_anio, expeYud.antecedente AS expeYud_antecedente, expeYud.extracto AS expeYud_extracto, expeYud.resolucion_iniciador AS expeYud_resolucion_iniciador, expeYud.iniciador AS expeYud_iniciador, expeYud.agregado AS expeYud_agregado, expeYud.lugar_iniciador AS expeYud_lugar_iniciador, expeYud.tema AS expeYud_tema, expeYud.ultimo_destino AS expeYud_ultimo_destino, 
expeYud_ini.id AS expeYud_ini_id, expeYud_ini.nombres AS expeYud_ini_nombres, expeYud_ini.apellidos AS expeYud_ini_apellidos, 
expeYud_agr.id AS expeYud_agr_id, expeYud_agr.numero AS expeYud_agr_numero, expeYud_agr.fecha_origen AS expeYud_agr_fecha_origen, expeYud_agr.fecha_entrada AS expeYud_agr_fecha_entrada, expeYud_agr.archivo_numero AS expeYud_agr_archivo_numero, expeYud_agr.archivo_anio AS expeYud_agr_archivo_anio, expeYud_agr.antecedente AS expeYud_agr_antecedente, expeYud_agr.extracto AS expeYud_agr_extracto, expeYud_agr.resolucion_iniciador AS expeYud_agr_resolucion_iniciador, expeYud_agr.iniciador AS expeYud_agr_iniciador, expeYud_agr.agregado AS expeYud_agr_agregado, expeYud_agr.lugar_iniciador AS expeYud_agr_lugar_iniciador, expeYud_agr.tema AS expeYud_agr_tema, expeYud_agr.ultimo_destino AS expeYud_agr_ultimo_destino, 
expeYud_agr_ini.id AS expeYud_agr_ini_id, expeYud_agr_ini.nombres AS expeYud_agr_ini_nombres, expeYud_agr_ini.apellidos AS expeYud_agr_ini_apellidos, 
expeYud_agr_li.id AS expeYud_agr_li_id, expeYud_agr_li.descripcion AS expeYud_agr_li_descripcion, 
expeYud_agr_tem.id AS expeYud_agr_tem_id, expeYud_agr_tem.descripcion AS expeYud_agr_tem_descripcion, 
expeYud_li.id AS expeYud_li_id, expeYud_li.descripcion AS expeYud_li_descripcion, 
expeYud_tem.id AS expeYud_tem_id, expeYud_tem.descripcion AS expeYud_tem_descripcion, 
      """


    """
     " concatenar campos principales en un campo alias label
    """
    def _fieldsLabel(self):
      return """ CONCAT_wS(', ', dest.fecha_entrada) AS label, 
"""

    #definir condicion de busqueda
    def _conditionSearch(self, search = None, alias = "dest"):
      if not search:
        return ''

      condition = ''
      #definir condiciones de id
      condition = condition + "(CAST(" + alias + ".id AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de fecha_entrada
      condition = condition + " OR "
      condition = condition + "(CAST(to_char(" + alias + ".fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de fecha_salida
      condition = condition + " OR "
      condition = condition + "(CAST(to_char(" + alias + ".fecha_salida, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de expediente
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".expediente AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de lugar
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".lugar AS CHAR) LIKE '%" + search + "%' ) "

      return "(" + condition + ")"

    """
     " definir condicion de busqueda avanzada
     " @param search Diccionario con los fields a buscar
     " @param connect Conexion
     " @param alias Alias de la tabla
     " @param fieldAlias Alias para identificar a los fields
    """
    def _conditionAdvancedSearch(self, connect, search = None, alias = "dest", fieldAlias = ""):
      if not search or "ic" not in search or int(float(search["ic"])) == 0:
        return ''

      condition = ''
      
      for i in range(0, int(float(search["ic"]))):
        i = str(i)
        #definir condiciones de id
        if search[i+"if"] == fieldAlias + "id": 
          condition = condition + "(" + alias + ".id = " + search[i+"iv"] + ") "

        #definir condiciones de expediente
        if search[i+"if"] == fieldAlias + "expediente": 
          if condition: 
            condition = condition + " " + connect + " "
          condition = condition + "(" + alias + ".expediente = " + search[i+"iv"] + ") "

        #definir condiciones de lugar
        if search[i+"if"] == fieldAlias + "lugar": 
          if condition: 
            condition = condition + " " + connect + " "
          condition = condition + "(" + alias + ".lugar = " + search[i+"iv"] + ") "

      return "(" + condition + ")"

    #fields de la tabla con cadena relaciones
    def _leftJoinsComplete(self):
      return """
LEFT OUTER JOIN expedientes.expediente AS exp ON (dest.expediente = exp.id)
LEFT OUTER JOIN expedientes.persona AS exp_ini ON (exp.iniciador = exp_ini.id)
LEFT OUTER JOIN expedientes.expediente AS exp_agr ON (exp.agregado = exp_agr.id)
LEFT OUTER JOIN expedientes.persona AS exp_agr_ini ON (exp_agr.iniciador = exp_agr_ini.id)
LEFT OUTER JOIN expedientes.lugar AS exp_agr_li ON (exp_agr.lugar_iniciador = exp_agr_li.id)
LEFT OUTER JOIN expedientes.tema AS exp_agr_tem ON (exp_agr.tema = exp_agr_tem.id)
LEFT OUTER JOIN expedientes.lugar AS exp_li ON (exp.lugar_iniciador = exp_li.id)
LEFT OUTER JOIN expedientes.tema AS exp_tem ON (exp.tema = exp_tem.id)
LEFT OUTER JOIN expedientes.lugar AS lug ON (dest.lugar = lug.id)
LEFT OUTER JOIN expedientes.expediente AS expeYud ON (dest.id = expeYud.ultimo_destino)
LEFT OUTER JOIN expedientes.persona AS expeYud_ini ON (expeYud.iniciador = expeYud_ini.id)
LEFT OUTER JOIN expedientes.expediente AS expeYud_agr ON (expeYud.agregado = expeYud_agr.id)
LEFT OUTER JOIN expedientes.persona AS expeYud_agr_ini ON (expeYud_agr.iniciador = expeYud_agr_ini.id)
LEFT OUTER JOIN expedientes.lugar AS expeYud_agr_li ON (expeYud_agr.lugar_iniciador = expeYud_agr_li.id)
LEFT OUTER JOIN expedientes.tema AS expeYud_agr_tem ON (expeYud_agr.tema = expeYud_agr_tem.id)
LEFT OUTER JOIN expedientes.lugar AS expeYud_li ON (expeYud.lugar_iniciador = expeYud_li.id)
LEFT OUTER JOIN expedientes.tema AS expeYud_tem ON (expeYud.tema = expeYud_tem.id)
      """

    def rowById(self, con, id):
        sql = "SELECT DISTINCT "
        sql = sql + self._fields()
        sql = sql + self._fieldsLabel()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.destino AS dest"
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

        sql = "SELECT "
        sql = sql + self._fields()
        sql = sql + self._fieldsComplete()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.destino AS dest"
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

        sql = "SELECT count(DISTINCT dest.id) AS num_rows"
        sql = sql + "	FROM expedientes.destino AS dest"
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

