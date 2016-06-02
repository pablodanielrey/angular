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
from model.users.users import User







if __name__ == '__main__':

    reg = inject.instance(Registry)
    
    silegConn = connection.Connection(reg.getRegistry('sileg'))
    dcsysConn = connection.Connection(reg.getRegistry('dcsys2'))
    
    conS = silegConn.get()
    curS = conS.cursor()
    
    conD = dcsysConn.get()

    try:
        curS.execute("""
          SELECT desig_observaciones, desig_fecha_desde, desig_fecha_hasta, desig_fecha_baja, tipocargo_nombre, tipodedicacion_nombre, tipocaracter_nombre, pers_nombres, pers_apellidos, pers_nrodoc, materia_nombre, catedra_nombre, dpto_nombre, lugdetrab_nombre, funcion_nombre
          FROM designacion_docente
          INNER JOIN tipo_cargo AS tc ON (desig_tipocargo_id = tipocargo_id)
          INNER JOIN tipo_dedicacion AS td ON (desig_tipodedicacion_id = tipodedicacion_id)
          INNER JOIN tipo_caracter AS tca ON (desig_tipocaracter_id = tipocaracter_id)
          INNER JOIN empleado ON (designacion_docente.desig_empleado_id = empleado.empleado_id)
          INNER JOIN persona ON (empleado.empleado_pers_id = persona.pers_id)
          LEFT OUTER JOIN catedras_x_materia ON (designacion_docente.desig_catxmat_id = catedras_x_materia.catxmat_id)
          LEFT OUTER JOIN materia ON (catedras_x_materia.catxmat_materia_id = materia.materia_id)
          LEFT OUTER JOIN catedra ON (catedras_x_materia.catxmat_catedra_id = catedra.catedra_id)
          LEFT OUTER JOIN departamento ON (materia.materia_dpto_id = departamento.dpto_id)
          LEFT OUTER JOIN lugar_de_trabajo ON (designacion_docente.desig_lugdetrab_id = lugar_de_trabajo.lugdetrab_id)
          LEFT OUTER JOIN area ON (lugar_de_trabajo.lugdetrab_area_id = area.area_id)
          LEFT OUTER JOIN funcion ON (designacion_docente.desig_funcion_id = funcion.funcion_id)
          LEFT OUTER JOIN extension ON (extension_designacion_id = desig_id)
          AND desig_fecha_baja IS NOT NULL
        """)

        for r in curS:
           
                       
            #definir "place" del tipo "departamento" a partir del campo dpto_nombre
            if(r["dpto_nombre"] is not None):
                place = Place()
                place.description = r["dpto_nombre"]
                place.type = "university center" if  any(x in r["dpto_nombre"].lower() for x in ["c.u", "c. u"]) else "department"                
                place.id = place.findByUnique(con = conD, description = place.description, type = place.type)
                place.persist(conD)

            #definir "place" del tipo "departamento" a partir del campo lugdetrab_nombre
            if r["lugdetrab_nombre"] is not None:
                place = Place()
                place.description = r["lugdetrab_nombre"]
                place.type = "department" if "departamento" in place.description.lower() else "office"
                place.id = place.findByUnique(con = conD, description = place.description, type = place.type)
                place.persist(conD)

            #definir "place" del tipo "catedra"
            if r["materia_nombre"] is not None:    
                catedra = " Catedra " + r["catedra_nombre"] if(r["catedra_nombre"] != 'Original') else ""
                
                place = Place()
                place.description = r["materia_nombre"] + catedra             
                place.type = "cathedra"
                place.dependence = None if(r["dpto_nombre"] is None) else place.findByUnique(con = conD, description = r["dpto_nombre"], type = "department")
                place.id = place.findByUnique(con = conD, description = place.description, type = place.type, dependence = place.dependence)
                place.persist(conD)
                
            
            #definir "position"
            cargo = r["tipocargo_nombre"]
            detail = r["tipocargo_nombre"] + " " + r["tipodedicacion_nombre"] + " " + r["tipocaracter_nombre"]
            
            position = Position()
            position.description = cargo
            position.detail = detail
            position.id = position.findByUnique(con = conD, description = position.description, detail = position.detail)
            position.persist(conD)


            #definir "usuario"
            user = User()
            res = user.findByDni(conD, str(r["pers_nrodoc"]))

            if res is None:
                user.name = r["pers_nombres"]
                user.lastname = r["pers_apellidos"]           
                user.dni = str(r["pers_nrodoc"])           
                user.id = user.persist(conD)
            else: 
                user.id = res[0]

            
            
            #definir "designation"
            designation = Designation()
            designation.start = r["desig_fecha_desde"]
            designation.end = r["desig_fecha_hasta"]
            designation.out = r["desig_fecha_baja"]
            designation.userId = user.id
            designation.placeId = place.id
            designation.positionId = position.id
            designation.persist(conD)
            
            conD.commit()
            

    finally:
        silegConn.put(conS)
        dcsysConn.put(conD)
        
        
    """
    conD = dcsysConn.get()
    silegConn.put(conS)
    """
