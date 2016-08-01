# -*- coding: utf-8 -*-
'''
    Implementación de un registro básico de preferencias
'''

import configparser
import os
import logging

class Registry:

    class SectionRegistry:
        ''' registro que saca los datos siempre de la misma sección '''
        def __init__(self, registry, section):
            self.registry = registry
            self.section = section

        def get(self, name):
            return self.registry._get(name, self.section)

    def __init__(self, name='registry.cfg'):
        self.home = home = os.path.expanduser("~")
        self.separator = os.path.sep
        self.preferences = configparser.ConfigParser()
        self.file = '{}{}{}'.format(self.home, self.separator, name)
        self.preferences.read(self.file)

    def _get(self, name, section='DEFAULT'):
        return self.preferences[section][name]

    def getRegistry(self, section):
        return self.SectionRegistry(self, section)

    def get(self, name):
        return self._get(name, 'DEFAULT')
