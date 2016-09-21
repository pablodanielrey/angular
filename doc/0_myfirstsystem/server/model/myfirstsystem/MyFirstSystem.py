
import logging
from model.myfirstsystem.entities.Message import Message
from model.myfirstsystem.entities.MyFirstEntity import MyFirstEntity

class MyFirstSystemModel:

    """
      Modelo del sistema
    """

    @classmethod
    def getMessage(cls):
        ##### Definir y retornar un mensaje #####
        message = Message()
        message.data = "Hola Mundo"
        return message


    @classmethod
    def helloWord(cls, con, param1, param2):
        ##### metodo de prueba que se conecta a AnotherEntity #####
        myFirstEntity = MyFirstEntity()
        myFirstEntity.attrib = param1
        myFirstEntity.persist(con)
        myFirstEntity.findByParam(con, param2)
        return myFirstEntity
       
       
         

