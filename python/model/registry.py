# -*- coding: utf-8 -*-
'''
    Implementación de un registro básico de preferencias
'''

import configparser
import os
import logging

class Registry:

    def __init__(self):
        self.home = home = os.path.expanduser("~")
        self.separator = os.path.sep
        self.preferences = configparser.ConfigParser()
        self.file = '{}{}{}'.format(self.home, self.separator, 'registry.cfg')
        self.preferences.read(self.file)

    def get(self, section, name):
        return self.preferences[section][name]
