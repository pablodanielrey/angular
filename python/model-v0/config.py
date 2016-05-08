# -*- coding: utf-8 -*-

from os.path import expanduser

import configparser
import logging

class Config:

    configs = {}

    def __init__(self,cfg):
        home = expanduser("~")
        cfg = home + '/' + cfg
        #logging.info("Reading config from : " + cfg)

        config = configparser.ConfigParser()
        config.read(cfg, encoding='UTF-8')
        for section in config.sections():
            options = config.options(section)
            for option in options:
                try:
                    value = config.get(section,option)
                    if value == 'True' or value == 'true':
                        value = True
                    elif value == 'False' or value == 'false':
                        value = False
                    self.configs[section + '_' + option] = value
                except:
                    self.configs[section + '_' + option] = None
