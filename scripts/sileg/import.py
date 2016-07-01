# -*- coding: utf-8 -*-
import sys
sys.path.append('../../python')

import inject
inject.configure()

import logging
logging.getLogger().setLevel(logging.INFO)



from model.registry import Registry
from model.connection import connection
from model.sileg.place.place import Place
from model.sileg.position.position import Position
from model.sileg.designation.designation import Designation
from model.sileg.designation.designation import OriginalDesignation
from model.sileg.designation.designation import Extension
from model.sileg.designation.designation import Prorogation
from model.sileg.designation.designation import ProrogationOriginal
from model.sileg.designation.designation import ProrogationExtension
from model.sileg.designation.designation import ClosedDesignation
from model.sileg.licence.licence import Licence
from model.users.users import User




class ImportSileg():


    @classmethod
    def placeFromDepartamento(cls, con, data):
        #definir "place" del tipo "departamento" a partir del campo dpto_nombre
        if(data["dpto_nombre"] is not None):
            place = Place()
            place.description = data["dpto_nombre"]
            place.type = "Centro Universitario" if  any(x in data["dpto_nombre"].lower() for x in ["c.u", "c. u"]) else "Departamento"
            place.id = place.findByUnique(con = con, description = place.description, type = place.type)
            place.persist(con)
            return place

        return None

    @classmethod
    def placeFromLugarTrabajo(cls, con, data):
        #definir "place" del tipo "departamento" a partir del campo lugdetrab_nombre
        if data["lugdetrab_nombre"] is not None:
            place = Place()
            place.description = data["lugdetrab_nombre"]
            place.type = data["area_nombre"]
            place.id = place.findByUnique(con = con, description = place.description, type = place.type)
            place.persist(con)
            return place

        return None


    @classmethod
    def placeFromCatedra(cls, con, data):
        #definir "place" del tipo "departamento" a partir del campo lugdetrab_nombre
        if data["materia_nombre"] is not None:
            catedra = " Catedra " + data["catedra_nombre"] if(data["catedra_nombre"] != 'Original') else ""

            place = Place()
            place.description = data["materia_nombre"] + catedra
            place.type = "Seminario" if "semi" in data["materia_nombre"].lower() else "Catedra"
            place.dependence = None if(data["dpto_nombre"] is None) else place.findByUnique(con = con, description = data["dpto_nombre"], type = "Departamento")
            place.id = place.findByUnique(con = con, description = place.description, type = place.type, dependence = place.dependence)
            place.persist(con)
            return place

        return None

    @classmethod
    def position(cls, con, data):
        #definir "position"
        cargo = data["tipocargo_nombre"]
        detail = data["tipocargo_nombre"] + " " + data["tipodedicacion_nombre"] + " " + data["tipocaracter_nombre"]

        position = Position()
        position.description = cargo
        position.detail = detail
        position.id = position.findByUnique(con = con, description = position.description, detail = position.detail)
        position.persist(con)

        return position


    @classmethod
    def user(cls, con, data):
        #definir "usuario"
        user = User()
        res = user.findByDni(con, str(data["pers_nrodoc"]))

        if res is None:
            user.name = data["pers_nombres"]
            user.lastname = data["pers_apellidos"]
            user.dni = str(data["pers_nrodoc"])
            user.id = user.persist(con)
        else:
            user.id = res[0]

        return user


    @classmethod
    def importOriginal(cls, con, userId, placeId, positionId, data):
        #definir "designation"
        designation = OriginalDesignation()
        designation.start = data["desig_fecha_desde"]
        designation.end = data["desig_fecha_hasta"]
        designation.out = data["desig_fecha_baja"]

        if data["resolucion_alta_numero"]:
            designation.resolution = data["resolucion_alta_numero"]
        if data["resolucion_alta_expediente"]:
            designation.record = data["resolucion_alta_expediente"]
   
   
        if data["resolucion_baja_numero"]:
            designation.oldResolutionOut = data["resolucion_baja_numero"]

        if data["resolucion_baja_expediente"]:
            designation.oldRecordOut = data["resolucion_baja_expediente"]
      
        
        designation.userId = userId
        designation.placeId = placeId
        designation.positionId = positionId
                
        designation.oldType = "des"
        designation.oldId = data["desig_id"]

        designation.id = designation.findByUnique(con, designation.oldId, designation.oldType)
        designation.persist(con)



    @classmethod
    def importExtension(cls, con, placeId, positionId, data):
        replaceId = Designation.findByUnique(conD, data["extension_designacion_id"], "des")

        if(replaceId is None):
            logging.info("Extension sin designacion " + str(data["extension_id"]))
            return

        replace = Designation.findById(conD, [replaceId])[0]

        #definir "designation"
        designation = Extension()
        designation.start = data["extension_fecha_desde"]
        designation.end = data["extension_fecha_hasta"]
        designation.out = data["extension_fecha_baja"]
        
        if not data["resolucion_alta_numero"]:
            designation.resolution = data["resolucion_alta_numero"]
        if not data["resolucion_alta_expediente"]:
            designation.record = data["resolucion_alta_expediente"]
            
        if data["resolucion_baja_numero"]:
            designation.oldResolutionOut = data["resolucion_baja_numero"]
        if data["resolucion_baja_expediente"]:
            designation.oldRecordOut = data["resolucion_baja_expediente"]
            
            
        designation.userId = replace.userId

        designation.placeId = placeId
        designation.positionId = positionId
        designation.replaceId = replace.id

        designation.oldType = "ext"
        designation.oldId = data["extension_id"]

        designation.id = designation.findByUnique(con, designation.oldId, designation.oldType)
        designation.persist(con)



    @classmethod
    def importDesignacionCatedra(cls, conS, conD):
        curS = conS.cursor()

        curS.execute("""
            SELECT desig_id, desig_observaciones, desig_fecha_desde, desig_fecha_hasta, desig_fecha_baja, 
            resolucion_alta.resolucion_numero AS resolucion_alta_numero,  resolucion_alta.resolucion_expediente AS resolucion_alta_expediente, 
            resolucion_baja.resolucion_numero AS resolucion_baja_numero,  resolucion_baja.resolucion_expediente AS resolucion_baja_expediente, 
            tipocargo_nombre, tipodedicacion_nombre, tipocaracter_nombre,
            pers_nombres, pers_apellidos, pers_nrodoc, 
            materia_nombre, catedra_nombre, 
            dpto_nombre
            FROM designacion_docente
            INNER JOIN tipo_cargo AS tc ON (desig_tipocargo_id = tipocargo_id)
            INNER JOIN tipo_dedicacion AS td ON (desig_tipodedicacion_id = tipodedicacion_id)
            INNER JOIN tipo_caracter AS tca ON (desig_tipocaracter_id = tipocaracter_id)
            INNER JOIN empleado ON (designacion_docente.desig_empleado_id = empleado.empleado_id)
            INNER JOIN persona ON (empleado.empleado_pers_id = persona.pers_id)
            INNER JOIN catedras_x_materia ON (designacion_docente.desig_catxmat_id = catedras_x_materia.catxmat_id)
            INNER JOIN materia ON (catedras_x_materia.catxmat_materia_id = materia.materia_id)
            INNER JOIN catedra ON (catedras_x_materia.catxmat_catedra_id = catedra.catedra_id)
            INNER JOIN departamento ON (materia.materia_dpto_id = departamento.dpto_id)
            LEFT JOIN resolucion AS resolucion_alta ON (resolucion_alta.resolucion_id = desig_resolucionalta_id)
            LEFT JOIN resolucion AS resolucion_baja ON (resolucion_baja.resolucion_id = desig_resolucionbaja_id);
        """)

        for r in curS:
            ImportSileg.placeFromDepartamento(conD, r)
            place = ImportSileg.placeFromCatedra(conD, r)

            position = ImportSileg.position(conD, r)

            user = ImportSileg.user(conD, r)

            ImportSileg.importOriginal(conD, user.id, place.id, position.id, r)

        conD.commit()



    @classmethod
    def importDesignacionLugarTrabajo(cls, conS, conD):
        curS = conS.cursor()

        curS.execute("""
            SELECT desig_id, desig_observaciones, desig_fecha_desde, desig_fecha_hasta, desig_fecha_baja,
            resolucion_alta.resolucion_numero AS resolucion_alta_numero,  resolucion_alta.resolucion_expediente AS resolucion_alta_expediente, 
            resolucion_baja.resolucion_numero AS resolucion_baja_numero,  resolucion_baja.resolucion_expediente AS resolucion_baja_expediente, 
            tipocargo_nombre, tipodedicacion_nombre, tipocaracter_nombre, pers_nombres, pers_apellidos, pers_nrodoc, lugdetrab_nombre, area_nombre, funcion_nombre
            FROM designacion_docente
            INNER JOIN tipo_cargo AS tc ON (desig_tipocargo_id = tipocargo_id)
            INNER JOIN tipo_dedicacion AS td ON (desig_tipodedicacion_id = tipodedicacion_id)
            INNER JOIN tipo_caracter AS tca ON (desig_tipocaracter_id = tipocaracter_id)
            INNER JOIN empleado ON (designacion_docente.desig_empleado_id = empleado.empleado_id)
            INNER JOIN persona ON (empleado.empleado_pers_id = persona.pers_id)
            INNER JOIN lugar_de_trabajo ON (designacion_docente.desig_lugdetrab_id = lugar_de_trabajo.lugdetrab_id)
            LEFT JOIN area ON (lugar_de_trabajo.lugdetrab_area_id = area.area_id)
            LEFT JOIN funcion ON (designacion_docente.desig_funcion_id = funcion.funcion_id)
            LEFT JOIN resolucion AS resolucion_alta ON (resolucion_alta.resolucion_id = desig_resolucionalta_id)
            LEFT JOIN resolucion AS resolucion_baja ON (resolucion_baja.resolucion_id = desig_resolucionbaja_id);
        """)

        for r in curS:
            place = ImportSileg.placeFromLugarTrabajo(conD, r)
            position = ImportSileg.position(conD, r)
            user = ImportSileg.user(conD, r)

            ImportSileg.importOriginal(conD, user.id, place.id, position.id, r)

        conD.commit()




    @classmethod
    def importExtensionCatedra(cls, conS, conD):

        curS = conS.cursor()

        ##### la implementacion actual requiere consultar el tipo cargo y el tipo caracter para definir la posicion!!!! #####
        curS.execute("""
            SELECT DISTINCT extension_id, extension_designacion_id, extension_fecha_desde, extension_fecha_hasta, extension_fecha_baja, 
            resolucion_alta.resolucion_numero AS resolucion_alta_numero,  resolucion_alta.resolucion_expediente AS resolucion_alta_expediente, 
            resolucion_baja.resolucion_numero AS resolucion_baja_numero,  resolucion_baja.resolucion_expediente AS resolucion_baja_expediente,
            tipocargo_nombre, tipocaracter_nombre, tipodedicacion_nombre, extension_fecha_baja, extension_catxmat_id, materia_nombre, catedra_nombre, dpto_nombre
            FROM extension e
            INNER JOIN designacion_docente dd ON (e.extension_designacion_id = dd.desig_id)
            INNER JOIN tipo_dedicacion AS td ON (e.extension_nuevadedicacion_id = td.tipodedicacion_id)
            INNER JOIN tipo_cargo tc ON (dd.desig_tipocargo_id = tc.tipocargo_id)
            INNER JOIN tipo_caracter AS tca ON (dd.desig_tipocaracter_id = tca.tipocaracter_id)
            INNER JOIN catedras_x_materia cxm ON (e.extension_catxmat_id = cxm.catxmat_id)
            INNER JOIN materia m ON (cxm.catxmat_materia_id = m.materia_id)
            INNER JOIN catedra c ON (cxm.catxmat_catedra_id = c.catedra_id)
            INNER JOIN departamento d ON (m.materia_dpto_id = d.dpto_id)
            LEFT JOIN resolucion AS resolucion_alta ON (resolucion_alta.resolucion_id = extension_resolucionalta_id)
            LEFT JOIN resolucion AS resolucion_baja ON (resolucion_baja.resolucion_id = extension_resolucionbaja_id);
        """)

        for r in curS:
            ImportSileg.placeFromDepartamento(conD, r)
            place = ImportSileg.placeFromCatedra(conD, r)
            position = ImportSileg.position(conD, r)

            ImportSileg.importExtension(conD, place.id, position.id, r)

        conD.commit()



    @classmethod
    def importExtensionLugarTrabajo(cls, conS, conD):
        curS = conS.cursor()

        ##### la implementacion actual requiere consultar el tipo cargo y el tipo caracter para definir la posicion!!!! #####
        curS.execute("""
            SELECT DISTINCT extension_id, extension_designacion_id, extension_fecha_desde, extension_fecha_hasta, extension_fecha_baja, 
            resolucion_alta.resolucion_numero AS resolucion_alta_numero,  resolucion_alta.resolucion_expediente AS resolucion_alta_expediente, 
            resolucion_baja.resolucion_numero AS resolucion_baja_numero,  resolucion_baja.resolucion_expediente AS resolucion_baja_expediente,
            tipocargo_nombre, tipocaracter_nombre, tipodedicacion_nombre, extension_fecha_baja,  lugdetrab_nombre, area_nombre, funcion_nombre
            FROM extension e
            INNER JOIN designacion_docente dd ON (e.extension_designacion_id = dd.desig_id)
            INNER JOIN tipo_dedicacion AS td ON (e.extension_nuevadedicacion_id = td.tipodedicacion_id)
            INNER JOIN tipo_cargo tc ON (dd.desig_tipocargo_id = tc.tipocargo_id)
            INNER JOIN tipo_caracter AS tca ON (dd.desig_tipocaracter_id = tca.tipocaracter_id)
            INNER JOIN empleado em ON (dd.desig_empleado_id = em.empleado_id)
            INNER JOIN persona p ON (em.empleado_pers_id = p.pers_id)
            INNER JOIN lugar_de_trabajo lc ON (e.extension_lugdetrab_id = lc.lugdetrab_id)
            LEFT JOIN area a ON (lc.lugdetrab_area_id =a.area_id)
            LEFT JOIN funcion f ON (e.extension_funcion_id = f.funcion_id)
            LEFT JOIN resolucion AS resolucion_alta ON (resolucion_alta.resolucion_id = extension_resolucionalta_id)
            LEFT JOIN resolucion AS resolucion_baja ON (resolucion_baja.resolucion_id = extension_resolucionbaja_id);
        """)

        for r in curS:
            place = ImportSileg.placeFromLugarTrabajo(conD, r)
            position = ImportSileg.position(conD, r)

            ImportSileg.importExtension(conD, place.id, position.id, r)

        conD.commit()

    @classmethod
    def importExtensionDesignacionCatedra(cls, conS, conD):
        curS = conS.cursor()

        ##### la implementacion actual requiere consultar el tipo cargo y el tipo caracter para definir la posicion!!!! #####
        curS.execute("""
            SELECT DISTINCT extension_id, extension_designacion_id, extension_fecha_desde, extension_fecha_hasta, extension_fecha_baja, 
            resolucion_alta.resolucion_numero AS resolucion_alta_numero,  resolucion_alta.resolucion_expediente AS resolucion_alta_expediente, 
            resolucion_baja.resolucion_numero AS resolucion_baja_numero,  resolucion_baja.resolucion_expediente AS resolucion_baja_expediente,          
            tipocargo_nombre, tipocaracter_nombre, tipodedicacion_nombre, extension_fecha_baja, extension_catxmat_id, materia_nombre, catedra_nombre, dpto_nombre
            FROM extension e
            INNER JOIN designacion_docente dd ON (e.extension_designacion_id = dd.desig_id)
            INNER JOIN tipo_dedicacion AS td ON (e.extension_nuevadedicacion_id = td.tipodedicacion_id)
            INNER JOIN tipo_cargo tc ON (dd.desig_tipocargo_id = tc.tipocargo_id)
            INNER JOIN tipo_caracter AS tca ON (dd.desig_tipocaracter_id = tca.tipocaracter_id)
            INNER JOIN catedras_x_materia cxm ON (dd.desig_catxmat_id = cxm.catxmat_id)
            INNER JOIN materia m ON (cxm.catxmat_materia_id = m.materia_id)
            INNER JOIN catedra c ON (cxm.catxmat_catedra_id = c.catedra_id)
            INNER JOIN departamento d ON (m.materia_dpto_id = d.dpto_id)
            LEFT JOIN resolucion AS resolucion_alta ON (resolucion_alta.resolucion_id = extension_resolucionalta_id)
            LEFT JOIN resolucion AS resolucion_baja ON (resolucion_baja.resolucion_id = extension_resolucionbaja_id)        
            WHERE (e.extension_catxmat_id IS NULL AND e.extension_lugdetrab_id IS NULL);
        """)

        for r in curS:
            ImportSileg.placeFromDepartamento(conD, r)
            place = ImportSileg.placeFromCatedra(conD, r)
            position = ImportSileg.position(conD, r)

            ImportSileg.importExtension(conD, place.id, position.id, r)

        conD.commit()


    @classmethod
    def importExtensionDesignacionLugarTrabajo(cls, conS, conD):
        curS = conS.cursor()

        ##### la implementacion actual requiere consultar el tipo cargo y el tipo caracter para definir la posicion!!!! #####
        curS.execute("""
          SELECT DISTINCT extension_id, extension_designacion_id, extension_fecha_desde, extension_fecha_hasta, extension_fecha_baja, 
            resolucion_alta.resolucion_numero AS resolucion_alta_numero, resolucion_alta.resolucion_expediente AS resolucion_alta_expediente, 
            resolucion_baja.resolucion_numero AS resolucion_baja_numero, resolucion_baja.resolucion_expediente AS resolucion_baja_expediente,
            tipocargo_nombre, tipocaracter_nombre, tipodedicacion_nombre, extension_fecha_baja,  lugdetrab_nombre, area_nombre, funcion_nombre
          FROM extension e
          INNER JOIN designacion_docente dd ON (e.extension_designacion_id = dd.desig_id)
          INNER JOIN tipo_dedicacion AS td ON (e.extension_nuevadedicacion_id = td.tipodedicacion_id)
          INNER JOIN tipo_cargo tc ON (dd.desig_tipocargo_id = tc.tipocargo_id)
          INNER JOIN tipo_caracter AS tca ON (dd.desig_tipocaracter_id = tca.tipocaracter_id)
          INNER JOIN empleado em ON (dd.desig_empleado_id = em.empleado_id)
          INNER JOIN persona p ON (em.empleado_pers_id = p.pers_id)
          INNER JOIN lugar_de_trabajo lc ON (dd.desig_lugdetrab_id = lc.lugdetrab_id)
          LEFT JOIN area a ON (lc.lugdetrab_area_id =a.area_id)
          LEFT JOIN funcion f ON (e.extension_funcion_id = f.funcion_id)
          LEFT JOIN resolucion AS resolucion_alta ON (resolucion_alta.resolucion_id = extension_resolucionalta_id)
          LEFT JOIN resolucion AS resolucion_baja ON (resolucion_baja.resolucion_id = extension_resolucionbaja_id)           
          WHERE (e.extension_catxmat_id IS NULL AND e.extension_lugdetrab_id IS NULL)
        """)

        for r in curS:
            place = ImportSileg.placeFromLugarTrabajo(conD, r)
            position = ImportSileg.position(conD, r)

            ImportSileg.importExtension(conD, place.id, position.id, r)

        conD.commit()


    @classmethod
    def _importProrroga(cls, conS, conD):
        curS = conS.cursor()

        curS.execute("""
            SELECT prorroga_id, prorroga_fecha_desde, prorroga_fecha_hasta, prorroga_fecha_baja, prorroga_prorroga_de, prorroga_prorroga_de_id,
            resolucion_alta.resolucion_numero AS resolucion_alta_numero,  resolucion_alta.resolucion_expediente AS resolucion_alta_expediente, 
            resolucion_baja.resolucion_numero AS resolucion_baja_numero,  resolucion_baja.resolucion_expediente AS resolucion_baja_expediente
            FROM prorroga
            LEFT JOIN resolucion AS resolucion_alta ON (resolucion_alta.resolucion_id = prorroga_resolucionalta_id)
            LEFT JOIN resolucion AS resolucion_baja ON (resolucion_baja.resolucion_id = prorroga_resolucionbaja_id)
            ORDER BY prorroga_fecha_desde, prorroga_fecha_hasta;
        """)

        for r in curS:
            replaceId = OriginalDesignation.findByUnique(conD, r["prorroga_prorroga_de_id"], r["prorroga_prorroga_de"])
            
            replace = None
            if(replaceId is not None):

                replace = OriginalDesignation.findById(conD, [replaceId])[0]
                replace.originalId = replace.id
                designation = ProrogationOriginal()
                
            if(replace is None):
                replaceId = ProrogationOriginal.findByUnique(conD, r["prorroga_prorroga_de_id"], r["prorroga_prorroga_de"])

                if(replaceId is not None):
                    replace = ProrogationOriginal.findById(conD, [replaceId])[0]
                    designation = ProrogationOriginal()
            
            if(replace is None):
                replaceId = Extension.findByUnique(conD, r["prorroga_prorroga_de_id"], r["prorroga_prorroga_de"])
                if(replaceId is not None):

                    replace = Extension.findById(conD, [replaceId])[0]
                    replace.originalId = replace.id
                    designation = ProrogationExtension()                
            
            if(replace is None):
                replaceId = ProrogationExtension.findByUnique(conD, r["prorroga_prorroga_de_id"], r["prorroga_prorroga_de"])
                if(replaceId is not None):

                    replace = ProrogationExtension.findById(conD, [replaceId])[0]
                    designation = ProrogationExtension()
            
            if(replace is None):
                continue
            
      
            designation.start = r["prorroga_fecha_desde"]
            designation.end = r["prorroga_fecha_hasta"]
            designation.userId = replace.userId
            designation.placeId = replace.placeId
            designation.positionId = replace.positionId
            designation.replaceId = replace.id
            designation.originalId = replace.originalId

            if not r["resolucion_alta_numero"]:
                designation.resolution = r["resolucion_alta_numero"]
            if not r["resolucion_alta_expediente"]:
                designation.record = r["resolucion_alta_expediente"]
            
            designation.oldResolutionOut = replace.oldResolutionOut
            designation.oldRecordOut = replace.oldRecordOut
            designation.oldId = r["prorroga_id"]
            designation.oldType = "pro"

            designation.id = designation.findByUnique(conD, designation.oldId, designation.oldType)
            designation.persist(conD)

        conD.commit()


    @classmethod
    def importProrroga(cls, conS, conD):
        curS = conS.cursor()

        numRowsOld = Prorogation.numRows(conD)

        while True:
            logging.info(numRowsOld)
            cls._importProrroga(conS, conD)
            numRows = Prorogation.numRows(conD)
            if numRows != numRowsOld:
                numRowsOld = numRows
            else:
                break




                
    @classmethod
    def importLicencia(cls, conS, conD):
        curS = conS.cursor()

        curS.execute("""
          SELECT licencia_id, licencia_designacion_id,licencia_fecha_desde, licencia_fecha_hasta, licencia_fecha_baja, licencia_articulo_id, licencia_tipolicencia_id, lc.licart_descripcion, licart_congocesueldo, tipolicencia_descripcion
          FROM licencia AS l
          LEFT JOIN licencia_articulos lc ON (lc.licart_id = l.licencia_articulo_id)
          INNER JOIN tipo_licencia tl ON (tl.tipolicencia_id = licencia_tipolicencia_id)
        """)

        for r in curS:
            designationId = Designation.findByUnique(conD, r["licencia_designacion_id"], "des")

            if(designationId is None):
                logging.info("Licencia sin designacion " + str(r["prorroga_id"]))
                continue

            licence = Licence()
            licence.start = r["licencia_fecha_desde"]
            licence.end = r["licencia_fecha_hasta"]
            licence.out = r["licencia_fecha_baja"]
            licence.designationId = designationId
            licence.description = r["tipolicencia_descripcion"] + ' ' if r["tipolicencia_descripcion"] != 'Licencia' else ''
            licence.oldId = r["licencia_id"]
            licence.oldType = "lic"
            licence.salary = True

            if(r["licencia_articulo_id"] is not None):
                licence.description = licence.description + r["licart_descripcion"]
                licence.salary = True if r["licart_congocesueldo"] == 1 else False


            licence.id = licence.findByUnique(conD, licence.oldId, licence.oldType)
            licence.persist(conD)

        conD.commit()

    @classmethod
    def importLicenceFromProrroga(cls, conS, conD):
        curS = conS.cursor()

        curS.execute("""
          SELECT prorroga_id, prorroga_fecha_desde, prorroga_fecha_hasta, prorroga_prorroga_de, prorroga_prorroga_de_id
          FROM prorroga
          ORDER BY prorroga_fecha_desde, prorroga_fecha_hasta
        """)

        for r in curS:
            licence = Licence()
            replaceId = licence.findByUnique(conD, r["prorroga_prorroga_de_id"], r["prorroga_prorroga_de"])

            if(replaceId is None):
                #logging.info("Prorroga sin licencia " + str(r["prorroga_id"]))
                continue

            replace = licence.findById(conD, [replaceId])[0]

            licence.start = r["prorroga_fecha_desde"]
            licence.end = r["prorroga_fecha_hasta"]
            licence.description = "prorroga"
            licence.salary = replace.salary
            licence.designationId = replace.designationId
            licence.replaceId = replace.id

            licence.oldId = r["prorroga_id"]
            licence.oldType = "pro"

            licence.id = licence.findByUnique(conD, licence.oldId, licence.oldType)
            licence.persist(conD)

        conD.commit()

    
    @classmethod
    def importClosed(cls, conD):       
        ids = Designation.findLastsAux(conD)
        designations = Designation.findById(conD, ids)
        
        for designation in designations:
            if designation.out:
              closed = ClosedDesignation()
              closed.start = designation.out
              closed.userId = designation.userId
              closed.placeId = designation.placeId
              closed.positionId = designation.positionId
              closed.resolution = designation.oldResolutionOut
              closed.record = designation.oldRecordOut
              closed.replaceId = designation.id
              closed.oldId = designation.oldId
              closed.oldType = designation.oldType + "_baja"
              closed.originalId = designation.originalId if designation.originalId is not None else designation.id
              
              closed.id = designation.findByUnique(conD, closed.oldId, closed.oldType)

              closed.persist(conD)

        conD.commit()
    
    @classmethod
    def importLicenceFromProrrogaCheckNumRows(cls, conS, conD):
        curS = conS.cursor()

        licence = Licence()
        numRowsOld = licence.numRowsByOldType(conD, "pro")

        while True:
            logging.info(numRowsOld)
            cls.importLicenceFromProrroga(conS, conD)
            numRows = licence.numRowsByOldType(conD, "pro")
            if numRows != numRowsOld:
                numRowsOld = numRows
            else:
                break

if __name__ == '__main__':

    import logging
    reg = inject.instance(Registry)

    silegConn = connection.Connection(reg.getRegistry('sileg'))
    dcsysConn = connection.Connection(reg.getRegistry('dcsys2'))

    conS = silegConn.get()
    try:
        conD = dcsysConn.get()
        try:
            """
            logging.info('importando designaciones de catedras')
            ImportSileg.importDesignacionCatedra(conS, conD)

            logging.info('importando designaciones de lugar de trabajo')
            ImportSileg.importDesignacionLugarTrabajo(conS, conD)
   
            logging.info('importando extensiones de catedras')
            ImportSileg.importExtensionCatedra(conS, conD)

            logging.info('importando extensiones de lugar de trabajo')
            ImportSileg.importExtensionLugarTrabajo(conS, conD)

            logging.info('importando extensiones de designaciones de catedras')
            ImportSileg.importExtensionDesignacionCatedra(conS, conD)

            logging.info('importando extensiones de las designaciones de lugar de trabajo')
            ImportSileg.importExtensionDesignacionLugarTrabajo(conS, conD)
            """
            logging.info('importando prorrogas')
            ImportSileg.importProrroga(conS, conD)
                        
            """
            logging.info('importando bajas')
            ImportSileg.importClosed(conD)
            

            logging.info('importando las licencias')
            ImportSileg.importLicencia(conS, conD)

            logging.info('importando las prorrogas de licencias')
            ImportSileg.importLicenceFromProrrogaCheckNumRows(conS, conD)
            """
        finally:
            dcsysConn.put(conD)

    finally:
        silegConn.put(conS)
