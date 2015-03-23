# -*- coding: utf-8 -*-


class Devices:

    """ TODO: por ahora por defecto hago que retorne para todos los dispositivos la zona de buenos aires. """
    def getTimeZone(self,id):
        """
            la zona retornada por pytz.all_timezones
        """
        return "America/Buenos_Aires"
