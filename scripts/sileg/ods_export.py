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
    
    conn = connection.Connection(reg.getRegistry('dcsys2'))
  
    con = conn.get()

    
    designation = Designation()
    designationIds = designation.findAllHistory(con)
    print(len(designationIds))
    designations = designation.findById(con, designationIds)
    
    
    place = Place()
    position = Position()

    calc = pyoo.Desktop('localhost', 2002)
    doc = calc.create_spreadsheet()
    sheet = doc.sheets[0]
    
       
    sheet[0,0].value = "id"
    sheet[0,1].value = "desde"
    sheet[0,2].value = "hasta"
    sheet[0,3].value = "baja"
    sheet[0,4].value = "cargo"
    sheet[0,5].value = "detalle"
    sheet[0,6].value = "lugar"
    sheet[0,7].value = "tipo"
    sheet[0,8].value = "dependencia"
    sheet[0,9].value = "reemplaza a"
    sheet[0,10].value = "licencia"
    sheet[0,11].value = "desde"
    sheet[0,12].value = "hasta"
    sheet[0,13].value = "baja"
    sheet[0,13].value = "reemplaza a"    
    
    licence = Licence()
        
    for row in range(0, len(designations)):
       places = place.findById(con, [designations[row].placeId])
       
       dependences = None if places[0].dependence is None else place.findById(con, [places[0].dependence])
       positions = position.findById(con, [designations[row].positionId])

       licenceIds = licence.findByDesignationId(con, designations[row].id)
       if(len(licenceIds) == 0):
           sheet[row+1,0].value = designations[row].id
           sheet[row+1,1].value = designations[row].start
           sheet[row+1,2].value = designations[row].end
           sheet[row+1,3].value = designations[row].out
           sheet[row+1,4].value = positions[0].description
           sheet[row+1,5].value = positions[0].detail
           sheet[row+1,6].value = places[0].description
           sheet[row+1,7].value = places[0].type
           sheet[row+1,8].value = "" if dependences is None else dependences[0].description + " (" + dependences[0].type + ")"       
           sheet[row+1,9].value = designations[row].replaceId
           sheet[row+1,10].value = ""
           sheet[row+1,11].value = ""           
           sheet[row+1,12].value = ""
           sheet[row+1,13].value = ""
       else:
           licences = licence.findById(con, licenceIds)
           for rowL in range(0, len(licences)):
               sheet[row+1,0].value = designations[row].id
               sheet[row+1,1].value = designations[row].start
               sheet[row+1,2].value = designations[row].end
               sheet[row+1,3].value = designations[row].out
               sheet[row+1,4].value = positions[0].description
               sheet[row+1,5].value = positions[0].detail
               sheet[row+1,6].value = places[0].description
               sheet[row+1,7].value = places[0].type
               sheet[row+1,8].value = "" if dependences is None else dependences[0].description + " (" + dependences[0].type + ")"       
               sheet[row+1,9].value = designations[row].replaceId
               sheet[row+1,10].value = licences[rowL].description
               sheet[row+1,11].value = licences[rowL].start
               sheet[row+1,12].value = licences[rowL].end
               sheet[row+1,13].value = licences[rowL].out
               sheet[row+1,13].value = licences[rowL].replaceId
       

       
    doc.save('/tmp/designations2.ods')
    doc.close()

