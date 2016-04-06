# -*- coding: utf-8 -*-
class Justification:

    @classmethod
    def getJustifications(cls, con, userIds, start, end):
        """
            obtiene todas las justificaciones para esos usuarios entre esas fechas.
            las fechas son datetime y son incluídos.
            retorna un mapa :
                justifications[useId] = [justification1, justification2, .... ]
        """
        ret = []
        for j in cls.__subclasses__():
            ret.extend(j.findByUserId(con, [userIds], start, end))

        return ret
