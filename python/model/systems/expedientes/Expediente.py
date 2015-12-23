# -*- coding: utf-8 -*-

import uuid, psycopg2, inject, psycopg2.extras
from model.utils import Tools

class Expediente:	

    #fields de la tabla
    def _fields(self):
      return """
expe.id AS id, expe.numero AS numero, expe.fecha_origen AS fecha_origen, expe.fecha_entrada AS fecha_entrada, expe.archivo_numero AS archivo_numero, expe.archivo_anio AS archivo_anio, expe.antecedente AS antecedente, expe.extracto AS extracto, expe.resolucion_iniciador AS resolucion_iniciador, expe.iniciador AS iniciador, expe.agregado AS agregado, expe.lugar_iniciador AS lugar_iniciador, expe.tema AS tema, expe.ultimo_destino AS ultimo_destino, 
"""

    #fields de la tabla y sus relaciones
    def _fieldsRelations(self):
      return """
expe.id AS id, expe.numero AS numero, expe.fecha_origen AS fecha_origen, expe.fecha_entrada AS fecha_entrada, expe.archivo_numero AS archivo_numero, expe.archivo_anio AS archivo_anio, expe.antecedente AS antecedente, expe.extracto AS extracto, expe.resolucion_iniciador AS resolucion_iniciador, expe.iniciador AS iniciador, expe.agregado AS agregado, expe.lugar_iniciador AS lugar_iniciador, expe.tema AS tema, expe.ultimo_destino AS ultimo_destino, 
ini.id AS ini_id, ini.nombres AS ini_nombres, ini.apellidos AS ini_apellidos, 
agr.id AS agr_id, agr.numero AS agr_numero, agr.fecha_origen AS agr_fecha_origen, agr.fecha_entrada AS agr_fecha_entrada, agr.archivo_numero AS agr_archivo_numero, agr.archivo_anio AS agr_archivo_anio, agr.antecedente AS agr_antecedente, agr.extracto AS agr_extracto, agr.resolucion_iniciador AS agr_resolucion_iniciador, agr.iniciador AS agr_iniciador, agr.agregado AS agr_agregado, agr.lugar_iniciador AS agr_lugar_iniciador, agr.tema AS agr_tema, agr.ultimo_destino AS agr_ultimo_destino, 
li.id AS li_id, li.descripcion AS li_descripcion, 
tem.id AS tem_id, tem.descripcion AS tem_descripcion, 
ud.id AS ud_id, ud.fecha_entrada AS ud_fecha_entrada, ud.fecha_salida AS ud_fecha_salida, ud.expediente AS ud_expediente, ud.lugar AS ud_lugar, 
"""

    #fields de la tabla con cadena relaciones
    def _fieldsComplete(self):
      return """
expe.id AS id, expe.numero AS numero, expe.fecha_origen AS fecha_origen, expe.fecha_entrada AS fecha_entrada, expe.archivo_numero AS archivo_numero, expe.archivo_anio AS archivo_anio, expe.antecedente AS antecedente, expe.extracto AS extracto, expe.resolucion_iniciador AS resolucion_iniciador, expe.iniciador AS iniciador, expe.agregado AS agregado, expe.lugar_iniciador AS lugar_iniciador, expe.tema AS tema, expe.ultimo_destino AS ultimo_destino, 
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


    """
     " concatenar campos principales en un campo alias label
    """
    def _fieldsLabel(self):
      return """CONCAT_WS(', ', expe.numero) AS label, 
"""

    #definir condicion de busqueda
    def _conditionSearch(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(expe.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expe.numero) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(expe.fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(expe.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.archivo_numero AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.archivo_anio AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expe.antecedente) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expe.extracto) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expe.resolucion_iniciador) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expe.iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.agregado AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.tema AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "
      return "(" + condition + ")"

    #definir condicion de busqueda
    def _conditionSearchRelations(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(expe.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expe.numero) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(expe.fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(expe.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.archivo_numero AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.archivo_anio AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expe.antecedente) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expe.extracto) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expe.resolucion_iniciador) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expe.iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.agregado AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.tema AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(ini.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(ini.nombres) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(ini.apellidos) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(agr.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(agr.numero) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(agr.fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(agr.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.archivo_numero AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.archivo_anio AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(agr.antecedente) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(agr.extracto) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(agr.resolucion_iniciador) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(agr.iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.agregado AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.tema AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(li.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(li.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(tem.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(tem.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(ud.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(ud.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(ud.fecha_salida, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(ud.expediente AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(ud.lugar AS CHAR) LIKE '%" + search + "%' ) "
      return "(" + condition + ")"

    #definir condicion de busqueda
    def _conditionSearchComplete(self, search = None):
      if not search:
        return ''

      condition = ''
      condition = condition + "(CAST(expe.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expe.numero) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(expe.fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(expe.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.archivo_numero AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.archivo_anio AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(expe.antecedente) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expe.extracto) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(expe.resolucion_iniciador) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(expe.iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.agregado AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.tema AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(expe.ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(ini.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(ini.nombres) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(ini.apellidos) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(agr.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(agr.numero) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(to_char(agr.fecha_origen, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(agr.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.archivo_numero AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.archivo_anio AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(agr.antecedente) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(agr.extracto) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(agr.resolucion_iniciador) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(agr.iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.agregado AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.lugar_iniciador AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.tema AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr.ultimo_destino AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr_ini.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(agr_ini.nombres) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (lower(agr_ini.apellidos) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(agr_li.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(agr_li.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(agr_tem.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(agr_tem.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(agr_ud.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(agr_ud.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(agr_ud.fecha_salida, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr_ud.expediente AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr_ud.lugar AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(agr_ud_lug.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(agr_ud_lug.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(li.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(li.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(tem.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(tem.descripcion) LIKE lower('%" + search + "%')) "
      condition = condition + " OR (CAST(ud.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(ud.fecha_entrada, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(to_char(ud.fecha_salida, '%d/%m/%Y') AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(ud.expediente AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(ud.lugar AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (CAST(ud_lug.id AS CHAR) LIKE '%" + search + "%' ) "
      condition = condition + " OR (lower(ud_lug.descripcion) LIKE lower('%" + search + "%')) "
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
          condition = condition + conn + "(expe.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "numero": 
          condition = condition + conn + "(lower(expe.numero) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "archivo_numero": 
          condition = condition + conn + "(expe.archivo_numero = " + search[i+"iv"] + ") "

        if search[i+"if"] == "archivo_anio": 
          condition = condition + conn + "(expe.archivo_anio = " + search[i+"iv"] + ") "

        if search[i+"if"] == "antecedente": 
          condition = condition + conn + "(lower(expe.antecedente) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "extracto": 
          condition = condition + conn + "(lower(expe.extracto) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "resolucion_iniciador": 
          condition = condition + conn + "(lower(expe.resolucion_iniciador) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "iniciador": 
          condition = condition + conn + "(expe.iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "agregado": 
          condition = condition + conn + "(expe.agregado = " + search[i+"iv"] + ") "

        if search[i+"if"] == "lugar_iniciador": 
          condition = condition + conn + "(expe.lugar_iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "tema": 
          condition = condition + conn + "(expe.tema = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ultimo_destino": 
          condition = condition + conn + "(expe.ultimo_destino = " + search[i+"iv"] + ") "

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
          condition = condition + conn + "(expe.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "numero": 
          condition = condition + conn + "(lower(expe.numero) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "archivo_numero": 
          condition = condition + conn + "(expe.archivo_numero = " + search[i+"iv"] + ") "

        if search[i+"if"] == "archivo_anio": 
          condition = condition + conn + "(expe.archivo_anio = " + search[i+"iv"] + ") "

        if search[i+"if"] == "antecedente": 
          condition = condition + conn + "(lower(expe.antecedente) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "extracto": 
          condition = condition + conn + "(lower(expe.extracto) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "resolucion_iniciador": 
          condition = condition + conn + "(lower(expe.resolucion_iniciador) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "iniciador": 
          condition = condition + conn + "(expe.iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "agregado": 
          condition = condition + conn + "(expe.agregado = " + search[i+"iv"] + ") "

        if search[i+"if"] == "lugar_iniciador": 
          condition = condition + conn + "(expe.lugar_iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "tema": 
          condition = condition + conn + "(expe.tema = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ultimo_destino": 
          condition = condition + conn + "(expe.ultimo_destino = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ini_id": 
          condition = condition + conn + "(ini.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ini_nombres": 
          condition = condition + conn + "(lower(ini.nombres) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "ini_apellidos": 
          condition = condition + conn + "(lower(ini.apellidos) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "agr_id": 
          condition = condition + conn + "(agr.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "agr_numero": 
          condition = condition + conn + "(lower(agr.numero) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "agr_archivo_numero": 
          condition = condition + conn + "(agr.archivo_numero = " + search[i+"iv"] + ") "

        if search[i+"if"] == "agr_archivo_anio": 
          condition = condition + conn + "(agr.archivo_anio = " + search[i+"iv"] + ") "

        if search[i+"if"] == "agr_antecedente": 
          condition = condition + conn + "(lower(agr.antecedente) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "agr_extracto": 
          condition = condition + conn + "(lower(agr.extracto) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "agr_resolucion_iniciador": 
          condition = condition + conn + "(lower(agr.resolucion_iniciador) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "agr_iniciador": 
          condition = condition + conn + "(agr.iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "agr_agregado": 
          condition = condition + conn + "(agr.agregado = " + search[i+"iv"] + ") "

        if search[i+"if"] == "agr_lugar_iniciador": 
          condition = condition + conn + "(agr.lugar_iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "agr_tema": 
          condition = condition + conn + "(agr.tema = " + search[i+"iv"] + ") "

        if search[i+"if"] == "agr_ultimo_destino": 
          condition = condition + conn + "(agr.ultimo_destino = " + search[i+"iv"] + ") "

        if search[i+"if"] == "li_id": 
          condition = condition + conn + "(li.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "li_descripcion": 
          condition = condition + conn + "(lower(li.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "tem_id": 
          condition = condition + conn + "(tem.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "tem_descripcion": 
          condition = condition + conn + "(lower(tem.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "ud_id": 
          condition = condition + conn + "(ud.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ud_expediente": 
          condition = condition + conn + "(ud.expediente = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ud_lugar": 
          condition = condition + conn + "(ud.lugar = " + search[i+"iv"] + ") "

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
          condition = condition + conn + "(expe.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "numero": 
          condition = condition + conn + "(lower(expe.numero) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "archivo_numero": 
          condition = condition + conn + "(expe.archivo_numero = " + search[i+"iv"] + ") "

        if search[i+"if"] == "archivo_anio": 
          condition = condition + conn + "(expe.archivo_anio = " + search[i+"iv"] + ") "

        if search[i+"if"] == "antecedente": 
          condition = condition + conn + "(lower(expe.antecedente) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "extracto": 
          condition = condition + conn + "(lower(expe.extracto) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "resolucion_iniciador": 
          condition = condition + conn + "(lower(expe.resolucion_iniciador) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "iniciador": 
          condition = condition + conn + "(expe.iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "agregado": 
          condition = condition + conn + "(expe.agregado = " + search[i+"iv"] + ") "

        if search[i+"if"] == "lugar_iniciador": 
          condition = condition + conn + "(expe.lugar_iniciador = " + search[i+"iv"] + ") "

        if search[i+"if"] == "tema": 
          condition = condition + conn + "(expe.tema = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ultimo_destino": 
          condition = condition + conn + "(expe.ultimo_destino = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ini_id": 
          condition = condition + conn + "(ini.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ini_nombres": 
          condition = condition + conn + "(lower(ini.nombres) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "ini_apellidos": 
          condition = condition + conn + "(lower(ini.apellidos) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "li_id": 
          condition = condition + conn + "(li.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "li_descripcion": 
          condition = condition + conn + "(lower(li.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "tem_id": 
          condition = condition + conn + "(tem.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "tem_descripcion": 
          condition = condition + conn + "(lower(tem.descripcion) = lower('" + search[i+"iv"] + "')) "

        if search[i+"if"] == "ud_id": 
          condition = condition + conn + "(ud.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ud_expediente": 
          condition = condition + conn + "(ud.expediente = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ud_lugar": 
          condition = condition + conn + "(ud.lugar = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ud_lug_id": 
          condition = condition + conn + "(ud_lug.id = " + search[i+"iv"] + ") "

        if search[i+"if"] == "ud_lug_descripcion": 
          condition = condition + conn + "(lower(ud_lug.descripcion) = lower('" + search[i+"iv"] + "')) "

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


    def orderByField(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'numero': 
            return 'numero ' + value
        if field == 'fecha_origen': 
            return 'fecha_origen ' + value
        if field == 'fecha_entrada': 
            return 'fecha_entrada ' + value
        if field == 'archivo_numero': 
            return 'archivo_numero ' + value
        if field == 'archivo_anio': 
            return 'archivo_anio ' + value
        if field == 'antecedente': 
            return 'antecedente ' + value
        if field == 'extracto': 
            return 'extracto ' + value
        if field == 'resolucion_iniciador': 
            return 'resolucion_iniciador ' + value
        if field == 'iniciador': 
            return 'iniciador ' + value
        if field == 'agregado': 
            return 'agregado ' + value
        if field == 'lugar_iniciador': 
            return 'lugar_iniciador ' + value
        if field == 'tema': 
            return 'tema ' + value
        if field == 'ultimo_destino': 
            return 'ultimo_destino ' + value

    def orderByFieldRelations(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'numero': 
            return 'numero ' + value
        if field == 'fecha_origen': 
            return 'fecha_origen ' + value
        if field == 'fecha_entrada': 
            return 'fecha_entrada ' + value
        if field == 'archivo_numero': 
            return 'archivo_numero ' + value
        if field == 'archivo_anio': 
            return 'archivo_anio ' + value
        if field == 'antecedente': 
            return 'antecedente ' + value
        if field == 'extracto': 
            return 'extracto ' + value
        if field == 'resolucion_iniciador': 
            return 'resolucion_iniciador ' + value
        if field == 'iniciador': 
            return 'iniciador ' + value
        if field == 'agregado': 
            return 'agregado ' + value
        if field == 'lugar_iniciador': 
            return 'lugar_iniciador ' + value
        if field == 'tema': 
            return 'tema ' + value
        if field == 'ultimo_destino': 
            return 'ultimo_destino ' + value
        if field == 'ini_id': 
            return 'ini_id ' + value
        if field == 'ini_nombres': 
            return 'ini_nombres ' + value
        if field == 'ini_apellidos': 
            return 'ini_apellidos ' + value
        if field == 'agr_id': 
            return 'agr_id ' + value
        if field == 'agr_numero': 
            return 'agr_numero ' + value
        if field == 'agr_fecha_origen': 
            return 'agr_fecha_origen ' + value
        if field == 'agr_fecha_entrada': 
            return 'agr_fecha_entrada ' + value
        if field == 'agr_archivo_numero': 
            return 'agr_archivo_numero ' + value
        if field == 'agr_archivo_anio': 
            return 'agr_archivo_anio ' + value
        if field == 'agr_antecedente': 
            return 'agr_antecedente ' + value
        if field == 'agr_extracto': 
            return 'agr_extracto ' + value
        if field == 'agr_resolucion_iniciador': 
            return 'agr_resolucion_iniciador ' + value
        if field == 'agr_iniciador': 
            return 'agr_iniciador ' + value
        if field == 'agr_agregado': 
            return 'agr_agregado ' + value
        if field == 'agr_lugar_iniciador': 
            return 'agr_lugar_iniciador ' + value
        if field == 'agr_tema': 
            return 'agr_tema ' + value
        if field == 'agr_ultimo_destino': 
            return 'agr_ultimo_destino ' + value
        if field == 'li_id': 
            return 'li_id ' + value
        if field == 'li_descripcion': 
            return 'li_descripcion ' + value
        if field == 'tem_id': 
            return 'tem_id ' + value
        if field == 'tem_descripcion': 
            return 'tem_descripcion ' + value
        if field == 'ud_id': 
            return 'ud_id ' + value
        if field == 'ud_fecha_entrada': 
            return 'ud_fecha_entrada ' + value
        if field == 'ud_fecha_salida': 
            return 'ud_fecha_salida ' + value
        if field == 'ud_expediente': 
            return 'ud_expediente ' + value
        if field == 'ud_lugar': 
            return 'ud_lugar ' + value

    def orderByFieldComplete(self, field, value):
        if field == 'id': 
            return 'id ' + value
        if field == 'numero': 
            return 'numero ' + value
        if field == 'fecha_origen': 
            return 'fecha_origen ' + value
        if field == 'fecha_entrada': 
            return 'fecha_entrada ' + value
        if field == 'archivo_numero': 
            return 'archivo_numero ' + value
        if field == 'archivo_anio': 
            return 'archivo_anio ' + value
        if field == 'antecedente': 
            return 'antecedente ' + value
        if field == 'extracto': 
            return 'extracto ' + value
        if field == 'resolucion_iniciador': 
            return 'resolucion_iniciador ' + value
        if field == 'iniciador': 
            return 'iniciador ' + value
        if field == 'agregado': 
            return 'agregado ' + value
        if field == 'lugar_iniciador': 
            return 'lugar_iniciador ' + value
        if field == 'tema': 
            return 'tema ' + value
        if field == 'ultimo_destino': 
            return 'ultimo_destino ' + value
        if field == 'ini_id': 
            return 'ini_id ' + value
        if field == 'ini_nombres': 
            return 'ini_nombres ' + value
        if field == 'ini_apellidos': 
            return 'ini_apellidos ' + value
        if field == 'li_id': 
            return 'li_id ' + value
        if field == 'li_descripcion': 
            return 'li_descripcion ' + value
        if field == 'tem_id': 
            return 'tem_id ' + value
        if field == 'tem_descripcion': 
            return 'tem_descripcion ' + value
        if field == 'ud_id': 
            return 'ud_id ' + value
        if field == 'ud_fecha_entrada': 
            return 'ud_fecha_entrada ' + value
        if field == 'ud_fecha_salida': 
            return 'ud_fecha_salida ' + value
        if field == 'ud_expediente': 
            return 'ud_expediente ' + value
        if field == 'ud_lugar': 
            return 'ud_lugar ' + value
        if field == 'ud_lug_id': 
            return 'ud_lug_id ' + value
        if field == 'ud_lug_descripcion': 
            return 'ud_lug_descripcion ' + value

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
        sql = sql + "	FROM expedientes.expediente AS expe"
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
        sql = sql + "	FROM expedientes.expediente AS expe"
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

        sql = "SELECT count(DISTINCT expe.id) AS num_rows"
        sql = sql + "	FROM expedientes.expediente AS expe"
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

