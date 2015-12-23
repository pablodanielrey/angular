# -*- coding: utf-8 -*-

import uuid, psycopg2, inject, psycopg2.extras
from model.utils import Tools

class Participacion:	

    #fields de la tabla
    def _fields(self):
      return """
part.id AS id, part.expediente AS expediente, part.persona AS persona, 
"""

    #fields de la tabla y sus relaciones
    def _fieldsRelations(self):
      return """
part.id AS id, part.expediente AS expediente, part.persona AS persona, 
exp.id AS exp_id, exp.numero AS exp_numero, exp.fecha_origen AS exp_fecha_origen, exp.fecha_entrada AS exp_fecha_entrada, exp.archivo_numero AS exp_archivo_numero, exp.archivo_anio AS exp_archivo_anio, exp.antecedente AS exp_antecedente, exp.extracto AS exp_extracto, exp.resolucion_iniciador AS exp_resolucion_iniciador, exp.iniciador AS exp_iniciador, exp.agregado AS exp_agregado, exp.lugar_iniciador AS exp_lugar_iniciador, exp.tema AS exp_tema, exp.ultimo_destino AS exp_ultimo_destino, 
per.id AS per_id, per.nombres AS per_nombres, per.apellidos AS per_apellidos, 
"""

    #fields de la tabla con cadena relaciones
    def _fieldsComplete(self):
      return """
part.id AS id, part.expediente AS expediente, part.persona AS persona, 
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
    def _conditionSearch(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(part.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(part.expediente AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(part.persona AS CHAR) LIKE '%" + search + "%' ) "
      return "(" + condition + ")"

    #definir condicion de busqueda
    def _conditionSearchRelations(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(part.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(part.expediente AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(part.persona AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp.numero) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(exp.fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(exp.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.archivo_numero AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.archivo_anio AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp.antecedente) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(exp.extracto) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(exp.resolucion_iniciador) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(exp.iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.agregado AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.tema AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(per.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(per.nombres) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(per.apellidos) LIKE lower('%" + search + "%')) "
      return "(" + condition + ")"

    #definir condicion de busqueda
    def _conditionSearchComplete(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(part.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(part.expediente AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(part.persona AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp.numero) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(exp.fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(exp.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.archivo_numero AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.archivo_anio AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp.antecedente) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(exp.extracto) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(exp.resolucion_iniciador) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(exp.iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.agregado AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.tema AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp.ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_ini.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_ini.nombres) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(exp_ini.apellidos) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(exp_agr.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_agr.numero) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(exp_agr.fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(exp_agr.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_agr.archivo_numero AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_agr.archivo_anio AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_agr.antecedente) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(exp_agr.extracto) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(exp_agr.resolucion_iniciador) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(exp_agr.iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_agr.agregado AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_agr.lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_agr.tema AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_agr.ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_agr_ini.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_agr_ini.nombres) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(exp_agr_ini.apellidos) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(exp_agr_li.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_agr_li.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(exp_agr_tem.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_agr_tem.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(exp_agr_ud.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(exp_agr_ud.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(exp_agr_ud.fecha_salida, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_agr_ud.expediente AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_agr_ud.lugar AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_agr_ud_lug.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_agr_ud_lug.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(exp_li.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_li.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(exp_tem.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_tem.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(exp_ud.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(exp_ud.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(exp_ud.fecha_salida, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_ud.expediente AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_ud.lugar AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(exp_ud_lug.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_ud_lug.descripcion) LIKE lower('%" + search + "%')) "
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
          condition = condition + conn + "(part.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expediente": 
          condition = condition + conn + "(part.expediente = " + search[i+"iv"] + ") "

        if search[i+"if"] == "persona": 
          condition = condition + conn + "(part.persona = " + search[i+"iv"] + ") "

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
          condition = condition + conn + "(part.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expediente": 
          condition = condition + conn + "(part.expediente = " + search[i+"iv"] + ") "

        if search[i+"if"] == "persona": 
          condition = condition + conn + "(part.persona = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_id": 
          condition = condition + conn + "(exp.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_numero": 
          condition = condition + conn + "(lower(exp.numero) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_archivo_numero": 
          condition = condition + conn + "(exp.archivo_numero = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_archivo_anio": 
          condition = condition + conn + "(exp.archivo_anio = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_antecedente": 
          condition = condition + conn + "(lower(exp.antecedente) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_extracto": 
          condition = condition + conn + "(lower(exp.extracto) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_resolucion_iniciador": 
          condition = condition + conn + "(lower(exp.resolucion_iniciador) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_iniciador": 
          condition = condition + conn + "(exp.iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_agregado": 
          condition = condition + conn + "(exp.agregado = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_lugar_iniciador": 
          condition = condition + conn + "(exp.lugar_iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_tema": 
          condition = condition + conn + "(exp.tema = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_ultimo_destino": 
          condition = condition + conn + "(exp.ultimo_destino = " + search[i+"iv"] + ") "

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
          condition = condition + conn + "(part.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expediente": 
          condition = condition + conn + "(part.expediente = " + search[i+"iv"] + ") "

        if search[i+"if"] == "persona": 
          condition = condition + conn + "(part.persona = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_id": 
          condition = condition + conn + "(exp.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_numero": 
          condition = condition + conn + "(lower(exp.numero) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_archivo_numero": 
          condition = condition + conn + "(exp.archivo_numero = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_archivo_anio": 
          condition = condition + conn + "(exp.archivo_anio = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_antecedente": 
          condition = condition + conn + "(lower(exp.antecedente) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_extracto": 
          condition = condition + conn + "(lower(exp.extracto) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_resolucion_iniciador": 
          condition = condition + conn + "(lower(exp.resolucion_iniciador) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_iniciador": 
          condition = condition + conn + "(exp.iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_agregado": 
          condition = condition + conn + "(exp.agregado = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_lugar_iniciador": 
          condition = condition + conn + "(exp.lugar_iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_tema": 
          condition = condition + conn + "(exp.tema = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_ultimo_destino": 
          condition = condition + conn + "(exp.ultimo_destino = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_ini_id": 
          condition = condition + conn + "(exp_ini.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_ini_nombres": 
          condition = condition + conn + "(lower(exp_ini.nombres) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_ini_apellidos": 
          condition = condition + conn + "(lower(exp_ini.apellidos) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_li_id": 
          condition = condition + conn + "(exp_li.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_li_descripcion": 
          condition = condition + conn + "(lower(exp_li.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_tem_id": 
          condition = condition + conn + "(exp_tem.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_tem_descripcion": 
          condition = condition + conn + "(lower(exp_tem.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "exp_ud_id": 
          condition = condition + conn + "(exp_ud.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_ud_expediente": 
          condition = condition + conn + "(exp_ud.expediente = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_ud_lugar": 
          condition = condition + conn + "(exp_ud.lugar = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_ud_lug_id": 
          condition = condition + conn + "(exp_ud_lug.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "exp_ud_lug_descripcion": 
          condition = condition + conn + "(lower(exp_ud_lug.descripcion) = lower('" + search[i+"iv"] + "')) "

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


    def orderByField(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'expediente': 
            return 'expediente ' + value
        if field == 'persona': 
            return 'persona ' + value

    def orderByFieldRelations(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'expediente': 
            return 'expediente ' + value
        if field == 'persona': 
            return 'persona ' + value
        if field == 'exp_id': 
            return 'exp_id ' + value
        if field == 'exp_numero': 
            return 'exp_numero ' + value
        if field == 'exp_fecha_origen': 
            return 'exp_fecha_origen ' + value
        if field == 'exp_fecha_entrada': 
            return 'exp_fecha_entrada ' + value
        if field == 'exp_archivo_numero': 
            return 'exp_archivo_numero ' + value
        if field == 'exp_archivo_anio': 
            return 'exp_archivo_anio ' + value
        if field == 'exp_antecedente': 
            return 'exp_antecedente ' + value
        if field == 'exp_extracto': 
            return 'exp_extracto ' + value
        if field == 'exp_resolucion_iniciador': 
            return 'exp_resolucion_iniciador ' + value
        if field == 'exp_iniciador': 
            return 'exp_iniciador ' + value
        if field == 'exp_agregado': 
            return 'exp_agregado ' + value
        if field == 'exp_lugar_iniciador': 
            return 'exp_lugar_iniciador ' + value
        if field == 'exp_tema': 
            return 'exp_tema ' + value
        if field == 'exp_ultimo_destino': 
            return 'exp_ultimo_destino ' + value
        if field == 'per_id': 
            return 'per_id ' + value
        if field == 'per_nombres': 
            return 'per_nombres ' + value
        if field == 'per_apellidos': 
            return 'per_apellidos ' + value

    def orderByFieldComplete(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'expediente': 
            return 'expediente ' + value
        if field == 'persona': 
            return 'persona ' + value
        if field == 'exp_id': 
            return 'exp_id ' + value
        if field == 'exp_numero': 
            return 'exp_numero ' + value
        if field == 'exp_fecha_origen': 
            return 'exp_fecha_origen ' + value
        if field == 'exp_fecha_entrada': 
            return 'exp_fecha_entrada ' + value
        if field == 'exp_archivo_numero': 
            return 'exp_archivo_numero ' + value
        if field == 'exp_archivo_anio': 
            return 'exp_archivo_anio ' + value
        if field == 'exp_antecedente': 
            return 'exp_antecedente ' + value
        if field == 'exp_extracto': 
            return 'exp_extracto ' + value
        if field == 'exp_resolucion_iniciador': 
            return 'exp_resolucion_iniciador ' + value
        if field == 'exp_iniciador': 
            return 'exp_iniciador ' + value
        if field == 'exp_agregado': 
            return 'exp_agregado ' + value
        if field == 'exp_lugar_iniciador': 
            return 'exp_lugar_iniciador ' + value
        if field == 'exp_tema': 
            return 'exp_tema ' + value
        if field == 'exp_ultimo_destino': 
            return 'exp_ultimo_destino ' + value
        if field == 'exp_ini_id': 
            return 'exp_ini_id ' + value
        if field == 'exp_ini_nombres': 
            return 'exp_ini_nombres ' + value
        if field == 'exp_ini_apellidos': 
            return 'exp_ini_apellidos ' + value
        if field == 'exp_li_id': 
            return 'exp_li_id ' + value
        if field == 'exp_li_descripcion': 
            return 'exp_li_descripcion ' + value
        if field == 'exp_tem_id': 
            return 'exp_tem_id ' + value
        if field == 'exp_tem_descripcion': 
            return 'exp_tem_descripcion ' + value
        if field == 'exp_ud_id': 
            return 'exp_ud_id ' + value
        if field == 'exp_ud_fecha_entrada': 
            return 'exp_ud_fecha_entrada ' + value
        if field == 'exp_ud_fecha_salida': 
            return 'exp_ud_fecha_salida ' + value
        if field == 'exp_ud_expediente': 
            return 'exp_ud_expediente ' + value
        if field == 'exp_ud_lugar': 
            return 'exp_ud_lugar ' + value
        if field == 'exp_ud_lug_id': 
            return 'exp_ud_lug_id ' + value
        if field == 'exp_ud_lug_descripcion': 
            return 'exp_ud_lug_descripcion ' + value
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
        sql = sql + "	FROM expedientes.participacion AS part"
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
        sql = sql + "	FROM expedientes.participacion AS part"
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

        sql = "SELECT count(DISTINCT part.id) AS num_rows"
        sql = sql + "	FROM expedientes.participacion AS part"
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

