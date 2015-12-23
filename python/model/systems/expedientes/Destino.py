# -*- coding: utf-8 -*-

import uuid, psycopg2, inject, psycopg2.extras
from model.utils import Tools

class Destino:	

    #fields de la tabla
    def _fields(self):
      return """
dest.id AS id, dest.fecha_entrada AS fecha_entrada, dest.fecha_salida AS fecha_salida, dest.expediente AS expediente, dest.lugar AS lugar, 
"""

    #fields de la tabla y sus relaciones
    def _fieldsRelations(self):
      return """
dest.id AS id, dest.fecha_entrada AS fecha_entrada, dest.fecha_salida AS fecha_salida, dest.expediente AS expediente, dest.lugar AS lugar, 
exp.id AS exp_id, exp.numero AS exp_numero, exp.fecha_origen AS exp_fecha_origen, exp.fecha_entrada AS exp_fecha_entrada, exp.archivo_numero AS exp_archivo_numero, exp.archivo_anio AS exp_archivo_anio, exp.antecedente AS exp_antecedente, exp.extracto AS exp_extracto, exp.resolucion_iniciador AS exp_resolucion_iniciador, exp.iniciador AS exp_iniciador, exp.agregado AS exp_agregado, exp.lugar_iniciador AS exp_lugar_iniciador, exp.tema AS exp_tema, exp.ultimo_destino AS exp_ultimo_destino, 
lug.id AS lug_id, lug.descripcion AS lug_descripcion, 
expeud.id AS expeud_id, expeud.numero AS expeud_numero, expeud.fecha_origen AS expeud_fecha_origen, expeud.fecha_entrada AS expeud_fecha_entrada, expeud.archivo_numero AS expeud_archivo_numero, expeud.archivo_anio AS expeud_archivo_anio, expeud.antecedente AS expeud_antecedente, expeud.extracto AS expeud_extracto, expeud.resolucion_iniciador AS expeud_resolucion_iniciador, expeud.iniciador AS expeud_iniciador, expeud.agregado AS expeud_agregado, expeud.lugar_iniciador AS expeud_lugar_iniciador, expeud.tema AS expeud_tema, expeud.ultimo_destino AS expeud_ultimo_destino, 
"""

    #fields de la tabla con cadena relaciones
    def _fieldsComplete(self):
      return """
dest.id AS id, dest.fecha_entrada AS fecha_entrada, dest.fecha_salida AS fecha_salida, dest.expediente AS expediente, dest.lugar AS lugar, 
exp.id AS exp_id, exp.numero AS exp_numero, exp.fecha_origen AS exp_fecha_origen, exp.fecha_entrada AS exp_fecha_entrada, exp.archivo_numero AS exp_archivo_numero, exp.archivo_anio AS exp_archivo_anio, exp.antecedente AS exp_antecedente, exp.extracto AS exp_extracto, exp.resolucion_iniciador AS exp_resolucion_iniciador, exp.iniciador AS exp_iniciador, exp.agregado AS exp_agregado, exp.lugar_iniciador AS exp_lugar_iniciador, exp.tema AS exp_tema, exp.ultimo_destino AS exp_ultimo_destino, 
exp_ini.id AS exp_ini_id, exp_ini.nombres AS exp_ini_nombres, exp_ini.apellidos AS exp_ini_apellidos, 
exp_agr.id AS exp_agr_id, exp_agr.numero AS exp_agr_numero, exp_agr.fecha_origen AS exp_agr_fecha_origen, exp_agr.fecha_entrada AS exp_agr_fecha_entrada, exp_agr.archivo_numero AS exp_agr_archivo_numero, exp_agr.archivo_anio AS exp_agr_archivo_anio, exp_agr.antecedente AS exp_agr_antecedente, exp_agr.extracto AS exp_agr_extracto, exp_agr.resolucion_iniciador AS exp_agr_resolucion_iniciador, exp_agr.iniciador AS exp_agr_iniciador, exp_agr.agregado AS exp_agr_agregado, exp_agr.lugar_iniciador AS exp_agr_lugar_iniciador, exp_agr.tema AS exp_agr_tema, exp_agr.ultimo_destino AS exp_agr_ultimo_destino, 
exp_agr_ini.id AS exp_agr_ini_id, exp_agr_ini.nombres AS exp_agr_ini_nombres, exp_agr_ini.apellidos AS exp_agr_ini_apellidos, 
exp_agr_li.id AS exp_agr_li_id, exp_agr_li.descripcion AS exp_agr_li_descripcion, 
exp_agr_tem.id AS exp_agr_tem_id, exp_agr_tem.descripcion AS exp_agr_tem_descripcion, 
exp_li.id AS exp_li_id, exp_li.descripcion AS exp_li_descripcion, 
exp_tem.id AS exp_tem_id, exp_tem.descripcion AS exp_tem_descripcion, 
lug.id AS lug_id, lug.descripcion AS lug_descripcion, 
expeud.id AS expeud_id, expeud.numero AS expeud_numero, expeud.fecha_origen AS expeud_fecha_origen, expeud.fecha_entrada AS expeud_fecha_entrada, expeud.archivo_numero AS expeud_archivo_numero, expeud.archivo_anio AS expeud_archivo_anio, expeud.antecedente AS expeud_antecedente, expeud.extracto AS expeud_extracto, expeud.resolucion_iniciador AS expeud_resolucion_iniciador, expeud.iniciador AS expeud_iniciador, expeud.agregado AS expeud_agregado, expeud.lugar_iniciador AS expeud_lugar_iniciador, expeud.tema AS expeud_tema, expeud.ultimo_destino AS expeud_ultimo_destino, 
expeud_ini.id AS expeud_ini_id, expeud_ini.nombres AS expeud_ini_nombres, expeud_ini.apellidos AS expeud_ini_apellidos, 
expeud_agr.id AS expeud_agr_id, expeud_agr.numero AS expeud_agr_numero, expeud_agr.fecha_origen AS expeud_agr_fecha_origen, expeud_agr.fecha_entrada AS expeud_agr_fecha_entrada, expeud_agr.archivo_numero AS expeud_agr_archivo_numero, expeud_agr.archivo_anio AS expeud_agr_archivo_anio, expeud_agr.antecedente AS expeud_agr_antecedente, expeud_agr.extracto AS expeud_agr_extracto, expeud_agr.resolucion_iniciador AS expeud_agr_resolucion_iniciador, expeud_agr.iniciador AS expeud_agr_iniciador, expeud_agr.agregado AS expeud_agr_agregado, expeud_agr.lugar_iniciador AS expeud_agr_lugar_iniciador, expeud_agr.tema AS expeud_agr_tema, expeud_agr.ultimo_destino AS expeud_agr_ultimo_destino, 
expeud_agr_ini.id AS expeud_agr_ini_id, expeud_agr_ini.nombres AS expeud_agr_ini_nombres, expeud_agr_ini.apellidos AS expeud_agr_ini_apellidos, 
expeud_agr_li.id AS expeud_agr_li_id, expeud_agr_li.descripcion AS expeud_agr_li_descripcion, 
expeud_agr_tem.id AS expeud_agr_tem_id, expeud_agr_tem.descripcion AS expeud_agr_tem_descripcion, 
expeud_li.id AS expeud_li_id, expeud_li.descripcion AS expeud_li_descripcion, 
expeud_tem.id AS expeud_tem_id, expeud_tem.descripcion AS expeud_tem_descripcion, 
"""


    """
     " concatenar campos principales en un campo alias label
    """
    def _fieldsLabel(self):
      return """CONCAT_WS(', ', dest.fecha_entrada) AS label, 
"""

    #definir condicion de busqueda
    def _conditionSearch(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(dest.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(dest.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(dest.fecha_salida, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(dest.expediente AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(dest.lugar AS CHAR) LIKE '%" + search + "%' ) "
      return "(" + condition + ")"

    #definir condicion de busqueda
    def _conditionSearchRelations(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(dest.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(dest.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(dest.fecha_salida, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(dest.expediente AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(dest.lugar AS CHAR) LIKE '%" + search + "%' ) "
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
      condition = condition + " OR (CAST(lug.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(lug.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expeud.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud.numero) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(expeud.fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(expeud.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.archivo_numero AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.archivo_anio AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud.antecedente) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expeud.extracto) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expeud.resolucion_iniciador) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expeud.iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.agregado AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.tema AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "
      return "(" + condition + ")"

    #definir condicion de busqueda
    def _conditionSearchComplete(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(dest.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(dest.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(dest.fecha_salida, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(dest.expediente AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(dest.lugar AS CHAR) LIKE '%" + search + "%' ) "
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
      condition = condition + " OR (CAST(exp_li.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_li.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(exp_tem.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(exp_tem.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(lug.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(lug.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expeud.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud.numero) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(expeud.fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(expeud.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.archivo_numero AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.archivo_anio AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud.antecedente) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expeud.extracto) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expeud.resolucion_iniciador) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expeud.iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.agregado AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.tema AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud.ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud_ini.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud_ini.nombres) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expeud_ini.apellidos) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expeud_agr.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud_agr.numero) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(expeud_agr.fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(expeud_agr.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud_agr.archivo_numero AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud_agr.archivo_anio AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud_agr.antecedente) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expeud_agr.extracto) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expeud_agr.resolucion_iniciador) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expeud_agr.iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud_agr.agregado AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud_agr.lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud_agr.tema AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud_agr.ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expeud_agr_ini.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud_agr_ini.nombres) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expeud_agr_ini.apellidos) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expeud_agr_li.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud_agr_li.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expeud_agr_tem.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud_agr_tem.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expeud_li.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud_li.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expeud_tem.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expeud_tem.descripcion) LIKE lower('%" + search + "%')) "
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
          condition = condition + conn + "(dest.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expediente": 
          condition = condition + conn + "(dest.expediente = " + search[i+"iv"] + ") "

        if search[i+"if"] == "lugar": 
          condition = condition + conn + "(dest.lugar = " + search[i+"iv"] + ") "

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
          condition = condition + conn + "(dest.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expediente": 
          condition = condition + conn + "(dest.expediente = " + search[i+"iv"] + ") "

        if search[i+"if"] == "lugar": 
          condition = condition + conn + "(dest.lugar = " + search[i+"iv"] + ") "

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

        if search[i+"if"] == "lug_id": 
          condition = condition + conn + "(lug.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "lug_descripcion": 
          condition = condition + conn + "(lower(lug.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_id": 
          condition = condition + conn + "(expeud.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_numero": 
          condition = condition + conn + "(lower(expeud.numero) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_archivo_numero": 
          condition = condition + conn + "(expeud.archivo_numero = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_archivo_anio": 
          condition = condition + conn + "(expeud.archivo_anio = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_antecedente": 
          condition = condition + conn + "(lower(expeud.antecedente) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_extracto": 
          condition = condition + conn + "(lower(expeud.extracto) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_resolucion_iniciador": 
          condition = condition + conn + "(lower(expeud.resolucion_iniciador) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_iniciador": 
          condition = condition + conn + "(expeud.iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_agregado": 
          condition = condition + conn + "(expeud.agregado = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_lugar_iniciador": 
          condition = condition + conn + "(expeud.lugar_iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_tema": 
          condition = condition + conn + "(expeud.tema = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_ultimo_destino": 
          condition = condition + conn + "(expeud.ultimo_destino = " + search[i+"iv"] + ") "

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
          condition = condition + conn + "(dest.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expediente": 
          condition = condition + conn + "(dest.expediente = " + search[i+"iv"] + ") "

        if search[i+"if"] == "lugar": 
          condition = condition + conn + "(dest.lugar = " + search[i+"iv"] + ") "

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

        if search[i+"if"] == "lug_id": 
          condition = condition + conn + "(lug.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "lug_descripcion": 
          condition = condition + conn + "(lower(lug.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_id": 
          condition = condition + conn + "(expeud.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_numero": 
          condition = condition + conn + "(lower(expeud.numero) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_archivo_numero": 
          condition = condition + conn + "(expeud.archivo_numero = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_archivo_anio": 
          condition = condition + conn + "(expeud.archivo_anio = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_antecedente": 
          condition = condition + conn + "(lower(expeud.antecedente) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_extracto": 
          condition = condition + conn + "(lower(expeud.extracto) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_resolucion_iniciador": 
          condition = condition + conn + "(lower(expeud.resolucion_iniciador) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_iniciador": 
          condition = condition + conn + "(expeud.iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_agregado": 
          condition = condition + conn + "(expeud.agregado = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_lugar_iniciador": 
          condition = condition + conn + "(expeud.lugar_iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_tema": 
          condition = condition + conn + "(expeud.tema = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_ultimo_destino": 
          condition = condition + conn + "(expeud.ultimo_destino = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_ini_id": 
          condition = condition + conn + "(expeud_ini.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_ini_nombres": 
          condition = condition + conn + "(lower(expeud_ini.nombres) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_ini_apellidos": 
          condition = condition + conn + "(lower(expeud_ini.apellidos) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_li_id": 
          condition = condition + conn + "(expeud_li.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_li_descripcion": 
          condition = condition + conn + "(lower(expeud_li.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "expeud_tem_id": 
          condition = condition + conn + "(expeud_tem.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "expeud_tem_descripcion": 
          condition = condition + conn + "(lower(expeud_tem.descripcion) = lower('" + search[i+"iv"] + "')) "

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
LEFT OUTER JOIN expedientes.expediente AS expeud ON (dest.id = expeud.ultimo_destino)
LEFT OUTER JOIN expedientes.persona AS expeud_ini ON (expeud.iniciador = expeud_ini.id)
LEFT OUTER JOIN expedientes.expediente AS expeud_agr ON (expeud.agregado = expeud_agr.id)
LEFT OUTER JOIN expedientes.persona AS expeud_agr_ini ON (expeud_agr.iniciador = expeud_agr_ini.id)
LEFT OUTER JOIN expedientes.lugar AS expeud_agr_li ON (expeud_agr.lugar_iniciador = expeud_agr_li.id)
LEFT OUTER JOIN expedientes.tema AS expeud_agr_tem ON (expeud_agr.tema = expeud_agr_tem.id)
LEFT OUTER JOIN expedientes.lugar AS expeud_li ON (expeud.lugar_iniciador = expeud_li.id)
LEFT OUTER JOIN expedientes.tema AS expeud_tem ON (expeud.tema = expeud_tem.id)
      """


    def orderByField(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'fecha_entrada': 
            return 'fecha_entrada ' + value
        if field == 'fecha_salida': 
            return 'fecha_salida ' + value
        if field == 'expediente': 
            return 'expediente ' + value
        if field == 'lugar': 
            return 'lugar ' + value

    def orderByFieldRelations(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'fecha_entrada': 
            return 'fecha_entrada ' + value
        if field == 'fecha_salida': 
            return 'fecha_salida ' + value
        if field == 'expediente': 
            return 'expediente ' + value
        if field == 'lugar': 
            return 'lugar ' + value
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
        if field == 'lug_id': 
            return 'lug_id ' + value
        if field == 'lug_descripcion': 
            return 'lug_descripcion ' + value
        if field == 'expeud_id': 
            return 'expeud_id ' + value
        if field == 'expeud_numero': 
            return 'expeud_numero ' + value
        if field == 'expeud_fecha_origen': 
            return 'expeud_fecha_origen ' + value
        if field == 'expeud_fecha_entrada': 
            return 'expeud_fecha_entrada ' + value
        if field == 'expeud_archivo_numero': 
            return 'expeud_archivo_numero ' + value
        if field == 'expeud_archivo_anio': 
            return 'expeud_archivo_anio ' + value
        if field == 'expeud_antecedente': 
            return 'expeud_antecedente ' + value
        if field == 'expeud_extracto': 
            return 'expeud_extracto ' + value
        if field == 'expeud_resolucion_iniciador': 
            return 'expeud_resolucion_iniciador ' + value
        if field == 'expeud_iniciador': 
            return 'expeud_iniciador ' + value
        if field == 'expeud_agregado': 
            return 'expeud_agregado ' + value
        if field == 'expeud_lugar_iniciador': 
            return 'expeud_lugar_iniciador ' + value
        if field == 'expeud_tema': 
            return 'expeud_tema ' + value
        if field == 'expeud_ultimo_destino': 
            return 'expeud_ultimo_destino ' + value

    def orderByFieldComplete(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'fecha_entrada': 
            return 'fecha_entrada ' + value
        if field == 'fecha_salida': 
            return 'fecha_salida ' + value
        if field == 'expediente': 
            return 'expediente ' + value
        if field == 'lugar': 
            return 'lugar ' + value
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
        if field == 'lug_id': 
            return 'lug_id ' + value
        if field == 'lug_descripcion': 
            return 'lug_descripcion ' + value
        if field == 'expeud_id': 
            return 'expeud_id ' + value
        if field == 'expeud_numero': 
            return 'expeud_numero ' + value
        if field == 'expeud_fecha_origen': 
            return 'expeud_fecha_origen ' + value
        if field == 'expeud_fecha_entrada': 
            return 'expeud_fecha_entrada ' + value
        if field == 'expeud_archivo_numero': 
            return 'expeud_archivo_numero ' + value
        if field == 'expeud_archivo_anio': 
            return 'expeud_archivo_anio ' + value
        if field == 'expeud_antecedente': 
            return 'expeud_antecedente ' + value
        if field == 'expeud_extracto': 
            return 'expeud_extracto ' + value
        if field == 'expeud_resolucion_iniciador': 
            return 'expeud_resolucion_iniciador ' + value
        if field == 'expeud_iniciador': 
            return 'expeud_iniciador ' + value
        if field == 'expeud_agregado': 
            return 'expeud_agregado ' + value
        if field == 'expeud_lugar_iniciador': 
            return 'expeud_lugar_iniciador ' + value
        if field == 'expeud_tema': 
            return 'expeud_tema ' + value
        if field == 'expeud_ultimo_destino': 
            return 'expeud_ultimo_destino ' + value
        if field == 'expeud_ini_id': 
            return 'expeud_ini_id ' + value
        if field == 'expeud_ini_nombres': 
            return 'expeud_ini_nombres ' + value
        if field == 'expeud_ini_apellidos': 
            return 'expeud_ini_apellidos ' + value
        if field == 'expeud_li_id': 
            return 'expeud_li_id ' + value
        if field == 'expeud_li_descripcion': 
            return 'expeud_li_descripcion ' + value
        if field == 'expeud_tem_id': 
            return 'expeud_tem_id ' + value
        if field == 'expeud_tem_descripcion': 
            return 'expeud_tem_descripcion ' + value

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
        orderBy = [{filterParams["of"]: filterParams["ot"]}] if "of" in filterParams else []

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

