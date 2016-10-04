# -*- coding: utf-8 -*-


'''
    Ejemplo de como implementar un registro de instancias de una clase en variables de clase
    usando métodos de clase y el constructor del objeto
'''


import logging

logging.getLogger().setLevel(logging.INFO)


class RegisterExample:

    clazzRegister = []

    @classmethod
    def register(cls,instance):
        if instance not in cls.clazzRegister:
            logging.info('registrando {} en la clase {}'.format(instance,cls))
            cls.clazzRegister.append(instance)


    @classmethod
    def unregister(cls,instance):
        if instance in cls.clazzRegister:
            logging.info('desregistrando {} en la clase {}'.format(instance,cls))
            cls.clazzRegister.remove(instance)


    def __init__(self):
        logging.info('instanciando {}'.format(self))
        self.__class__.register(self)




if __name__ == '__main__':

    r = RegisterExample()
    logging.info(r.__class__.clazzRegister)
    r.__class__.unregister(r)
