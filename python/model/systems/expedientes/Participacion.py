# -*- coding: utf-8 -*-

import uuid, psycopg2, inject, psycopg2.extras
from model.utils import Tools

class Participacion:	

    #fields de la tabla
    def _fields(self):
      return """
part.id AS id, part.expediente AS expediente, part.persona AS persona, 
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
exp_agr_ud.id AS exp_agr_ud_id, exp_agr_ud.fecha_entrada AS exp_agr_ud_fecha_entrada, exp_agr_ud.fecha_salida AS exp_agr_ud_fecha_salida, exp_agr_ud.expediente AS exp_agr_ud_expediente, exp_agr_ud.lugar AS exp_agr_ud_lugar, 
exp_agr_ud_lug.id AS exp_agr_ud_lug_id, exp_agr_ud_lug.descripcion AS exp_agr_ud_lug_descripcion, 
exp_li.id AS exp_li_id, exp_li.descripcion AS exp_li_descripcion, 
exp_tem.id AS exp_tem_id, exp_tem.descripcion AS exp_tem_descripcion, 
exp_ud.id AS exp_ud_id, exp_ud.fecha_entrada AS exp_ud_fecha_entrada, exp_ud.fecha_salida AS exp_ud_fecha_salida, exp_ud.expediente AS exp_ud_expediente, exp_ud.lugar AS exp_ud_lugar, 
exp_ud_lug.id AS exp_ud_lug_id, exp_ud_lug.descripcion AS exp_ud_lug_descripcion, 
per.id AS per_id, per.nombres AS per_nombres, per.apellidos AS per_apellidos, 
      """

    #definir condicion de busqueda
    def _conditionSearch(self, search = None, alias = "part"):
      if not search:
        return ''

      condition = ''
      #definir condiciones de id
      condition = condition + "(CAST(" + alias + ".id AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de expediente
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".expediente AS CHAR) LIKE '%" + search + "%' ) "

      #definir condiciones de persona
      condition = condition + " OR "
      condition = condition + "(CAST(" + alias + ".persona AS CHAR) LIKE '%" + search + "%' ) "

      return "(" + condition + ")"

    #fields de la tabla con cadena relaciones
    def _leftJoinsComplete(self):
      return """
LEFT OUTER JOIN expedientes.expediente AS exp ON (part.expediente = exp.id)
LEFT OUTER JOIN expedientes.persona AS exp_ini ON (exp.iniciador = exp_ini.id)
LEFT OUTER JOIN expedientes.expediente AS exp_agr ON (exp.agregado = exp_agr.id)
LEFT OUTER JOIN expedientes.persona AS exp_agr_ini ON (exp_agr.iniciador = exp_agr_ini.id)
LEFT OUTER JOIN expedientes.lugar AS exp_agr_li ON (exp_agr.lugar_iniciador = exp_agr_li.id)
LEFT OUTER JOIN expedientes.tema AS exp_agr_tem ON (exp_agr.tema = exp_agr_tem.id)
LEFT OUTER JOIN expedientes.destino AS exp_agr_ud ON (exp_agr.ultimo_destino = exp_agr_ud.id)
LEFT OUTER JOIN expedientes.lugar AS exp_agr_ud_lug ON (exp_agr_ud.lugar = exp_agr_ud_lug.id)
LEFT OUTER JOIN expedientes.lugar AS exp_li ON (exp.lugar_iniciador = exp_li.id)
LEFT OUTER JOIN expedientes.tema AS exp_tem ON (exp.tema = exp_tem.id)
LEFT OUTER JOIN expedientes.destino AS exp_ud ON (exp.ultimo_destino = exp_ud.id)
LEFT OUTER JOIN expedientes.lugar AS exp_ud_lug ON (exp_ud.lugar = exp_ud_lug.id)
LEFT OUTER JOIN expedientes.persona AS per ON (part.persona = per.id)
      """

    def rowById(self, con, id):
        sql = "SELECT DISTINCT "
        sql = sql + self._fields()
        sql = sql[:sql.rfind(",")] #eliminar ultima coma
        sql = sql + "	FROM expedientes.participacion AS part"
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
        sql = sql + "	FROM expedientes.participacion AS part"
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
        sql = "SELECT count(DISTINCT part.id) AS num_rows"
        sql = sql + "	FROM expedientes.participacion AS part"
        sql = sql + self._leftJoinsComplete()
        cond = self._conditionSearch(search)
        sql = sql + Tools.concat(cond, 'WHERE')

        cur = con.cursor()
        cur.execute(sql)
        if cur.rowcount <= 0:
            return None
            
        return cur.fetchone()[0]

