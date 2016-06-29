# -*- coding: utf-8 -*-
import sys
sys.path.append('../../python')

import inject
inject.configure()

import logging
logging.getLogger().setLevel(logging.INFO)

import pyoo

from model.registry import Registry
from model.connection import connection
from model.sileg.place.place import Place
from model.sileg.position.position import Position
from model.sileg.designation.designation import Designation
from model.sileg.licence.licence import Licence
from model.users.users import User




if __name__ == '__main__':

    reg = inject.instance(Registry)

    logging.info('Obteniendo la conexion')
    conn = connection.Connection(reg.getRegistry('dcsys2'))
    con = conn.get()
    try:

        designation = Designation()
        designationIds = designation.findLasts(con)
        if len(designationIds) <= 0:
            logging.info('no se encontraron designaciones')
            sys.exit(1)

        logging.info('obteniendo todas las designaciones {}'.format(len(designationIds)))
        designations = designation.findById(con, designationIds)

        calc = pyoo.Desktop('localhost', 2002)
        doc = calc.create_spreadsheet()
        try:
            sheet = doc.sheets[0]

            sheet[0,0].value = "id"
            sheet[0,1].value = "desde"
            sheet[0,2].value = "hasta"
            sheet[0,3].value = "baja"
            sheet[0,4].value = "nombres"
            sheet[0,5].value = "apellidos"
            sheet[0,6].value = "dni"
            sheet[0,7].value = "cargo"
            sheet[0,8].value = "detalle"
            sheet[0,9].value = "lugar"
            sheet[0,10].value = "tipo"
            sheet[0,11].value = "dependencia"
            sheet[0,12].value = "reemplaza a"
            sheet[0,13].value = "licencia"
            sheet[0,14].value = "desde"
            sheet[0,15].value = "hasta"
            sheet[0,16].value = "baja"
            sheet[0,17].value = "reemplaza a"
            sheet[0,18].value = "descripcion"

            row = 0
            for designation in designations:
               row = row + 1
               logging.info('exportando {}'.format(designation.__dict__))
               places = Place.findById(con, [designation.placeId])
               users = User.findById(con, [designation.userId])

               dependences = None if places[0].dependence is None else Place.findById(con, [places[0].dependence])
               positions = Position.findById(con, [designation.positionId])

               licenceIds = Licence.findByDesignationId(con, designation.id)
               if(len(licenceIds) == 0):
                   sheet[row+1,0].value = designation.id
                   sheet[row+1,1].value = designation.start
                   sheet[row+1,2].value = designation.end
                   sheet[row+1,3].value = designation.out
                   sheet[row+1,4].value = users[0].name
                   sheet[row+1,5].value = users[0].lastname
                   sheet[row+1,6].value = users[0].dni
                   sheet[row+1,7].value = positions[0].description
                   sheet[row+1,8].value = positions[0].detail
                   sheet[row+1,9].value = places[0].description
                   sheet[row+1,10].value = places[0].type
                   sheet[row+1,11].value = "" if dependences is None else dependences[0].description + " (" + dependences[0].type + ")"
                   sheet[row+1,12].value = designation.replaceId
                   sheet[row+1,13].value = ""
                   sheet[row+1,14].value = ""
                   sheet[row+1,15].value = ""
                   sheet[row+1,16].value = ""
                   sheet[row+1,17].value = ""
                   sheet[row+1,18].value = designation.description
               else:
                   licences = Licence.findById(con, licenceIds)
                   for rowL in range(0, len(licences)):
                       sheet[row+1,0].value = designation.id
                       sheet[row+1,1].value = designation.start
                       sheet[row+1,2].value = designation.end
                       sheet[row+1,3].value = designation.out
                       sheet[row+1,4].value = users[0].name
                       sheet[row+1,5].value = users[0].lastname
                       sheet[row+1,6].value = users[0].dni
                       sheet[row+1,7].value = positions[0].description
                       sheet[row+1,8].value = positions[0].detail
                       sheet[row+1,9].value = places[0].description
                       sheet[row+1,10].value = places[0].type
                       sheet[row+1,11].value = "" if dependences is None else dependences[0].description + " (" + dependences[0].type + ")"
                       sheet[row+1,12].value = designation.replaceId
                       sheet[row+1,13].value = licences[rowL].description
                       sheet[row+1,14].value = licences[rowL].start
                       sheet[row+1,15].value = licences[rowL].end
                       sheet[row+1,16].value = licences[rowL].out
                       sheet[row+1,17].value = licences[rowL].replaceId
                       sheet[row+1,18].value = designation.description
            doc.save('/tmp/designations2.ods')

        finally:
            doc.close()

    finally:
        conn.put(con)
