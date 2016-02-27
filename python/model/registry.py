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

    @staticmethod
    def _getSectionName(instance):
        if instance.__class__.__name__ == 'type':
            return '{}.{}'.format(instance.__module__, self.__name__)
        else:
            return '{}.{}'.format(instance.__class__.__module__, self.__class__.__name__)

    def get(self, instance, name):
        setion = Registry._getSectionName(instance)
        return self.preferences[section][name]

    def get(self, name):
        return self.preferences['DEFAULT'][name]
