# -*- coding: utf-8 -*-

import uuid, psycopg2, inject, psycopg2.extras
from model.utils import Tools

class Expediente:	

    #fields de la tabla
    def _fields(self):
      return """
expe.id AS id, expe.numero AS numero, expe.fecha_origen AS fecha_origen, expe.fecha_entrada AS fecha_entrada, expe.archivo_numero AS archivo_numero, expe.archivo_anio AS archivo_anio, expe.antecedente AS antecedente, expe.extracto AS extracto, expe.resolucion_iniciador AS resolucion_iniciador, expe.iniciador AS iniciador, expe.agregado AS agregado, expe.lugar_iniciador AS lugar_iniciador, expe.tema AS tema, expe.ultimo_destino AS ultimo_destino, 
      """

    #fields de la tabla con cadena relaciones
    def _fieldsComplete(self):
      return """
ini.id AS ini_id, ini.nombres AS ini_nombres, ini.apellidos AS ini_apellidos, 
agr.id AS agr_id, agr.numero AS agr_numero, agr.fecha_origen AS agr_fecha_origen, agr.fecha_entrada AS agr_fecha_entrada, agr.archivo_numero AS agr_archivo_numero, agr.archivo_anio AS agr_archivo_anio, agr.antecedente AS agr_antecedente, agr.extracto AS agr_extracto, agr.resolucion_iniciador AS agr_resolucion_iniciador, agr.iniciador AS agr_iniciador, agr.agregado AS agr_agregado, agr.lugar_iniciador AS agr_lugar_iniciador, agr.tema AS agr_tema, agr.ultimo_destino AS agr_ultimo_destino, 
agr_ini.id AS agr_ini_id, agr_ini.nombres AS agr_ini_nombres, agr_ini.apellidos AS agr_ini_apellidos, 
agr_li.id AS agr_li_id, agr_li.descripcion AS agr_li_descripcion, 
agr_tem.id AS agr_tem_id, agr_tem.descripcion AS agr_tem_descripcion, 
agr_ud.id AS agr_ud_id, agr_ud.fecha_entrada AS agr_ud_fecha_entrada, agr_ud.fecha_salida AS agr_ud_fecha_salida, agr_ud.expediente AS agr_ud_expediente, agr_ud.lugar AS agr_ud_lugar, 
agr_ud_lug.id AS agr_ud_lug_id, agr_ud_lug.descripcion AS agr_ud_lug_descripcion, 
li.id AS li_id, li.descripcion AS li_descripcion, 
tem.id AS tem_id, tem.descripcion AS tem_descripcion, 
ud.id AS ud_id, ud.fecha_entrada AS ud_fecha_entrada, ud.fecha_salida AS ud_fecha_salida, ud.expediente AS ud_expediente, ud.lugar AS ud_lugar, 
ud_lug.id AS ud_lug_id, ud_lug.descripcion AS ud_lug_descripcion, 
      """

    #definir condicion de busqueda
    def _conditionSearch(self, search = None, alias = "expe"):
      if not search:
        return ''

      condition = ''
      #definir condiciones de id
      condition = condition + "(CAST(" + alias + ".id AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de numero
      condition = condition + " OR "
      condition = condition + "(lower(" + alias + ".numero) LIKE lower('%" + search + "%')) "
      #definir condiciones de fecha_origen
      condition = condition + " OR "
      condition = condition + "(CAST(to_char(" + alias + ".fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de fecha_entrada
      condition = condition + " OR "
      condition = condition + "(CAST(to_char(" + alias + ".fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de archivo_numero
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".archivo_numero AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de archivo_anio
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".archivo_anio AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de antecedente
      condition = condition + " OR "
      condition = condition + "(lower(" + alias + ".antecedente) LIKE lower('%" + search + "%')) "
      #definir condiciones de extracto
      condition = condition + " OR "
      condition = condition + "(lower(" + alias + ".extracto) LIKE lower('%" + search + "%')) "
      #definir condiciones de resolucion_iniciador
      condition = condition + " OR "
      condition = condition + "(lower(" + alias + ".resolucion_iniciador) LIKE lower('%" + search + "%')) "
      #definir condiciones de iniciador
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".iniciador AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de agregado
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".agregado AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de lugar_iniciador
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de tema
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".tema AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de ultimo_destino
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "

      return "(" + condition + ")"

    #fields de la tabla con cadena relaciones
    def _leftJoinsComplete(self):
      return """
LEFT OUTER JOIN expedientes.persona AS ini ON (expe.iniciador = ini.id)
LEFT OUTER JOIN expedientes.expediente AS agr ON (expe.agregado = agr.id)
LEFT OUTER JOIN expedientes.persona AS agr_ini ON (agr.iniciador = agr_ini.id)
LEFT OUTER JOIN expedientes.lugar AS agr_li ON (agr.lugar_iniciador = agr_li.id)
LEFT OUTER JOIN expedientes.tema AS agr_tem ON (agr.tema = agr_tem.id)
LEFT OUTER JOIN expedientes.destino AS agr_ud ON (agr.ultimo_destino = agr_ud.id)
LEFT OUTER JOIN expedientes.lugar AS agr_ud_lug ON (agr_ud.lugar = agr_ud_lug.id)
LEFT OUTER JOIN expedientes.lugar AS li ON (expe.lugar_iniciador = li.id)
LEFT OUTER JOIN expedientes.tema AS tem ON (expe.tema = tem.id)
LEFT OUTER JOIN expedientes.destino AS ud ON (expe.ultimo_destino = ud.id)
LEFT OUTER JOIN expedientes.lugar AS ud_lug ON (ud.lugar = ud_lug.id)
      """

    def rowById(self, con, id):
        sql = "SELECT DISTINCT "
        sql = sql + self._fields()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.expediente AS expe"
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
        sql = sql + "	FROM expedientes.expediente AS expe"
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
        sql = "SELECT count(DISTINCT expe.id) AS num_rows"
        sql = sql + "	FROM expedientes.expediente AS expe"
        sql = sql + self._leftJoinsComplete()
        cond = self._conditionSearch(search)
        sql = sql + Tools.concat(cond, 'WHERE')

        cur = con.cursor()
        cur.execute(sql)
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()[0]

