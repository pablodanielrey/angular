# -*- coding: utf-8 -*-

from os.path import expanduser

import configparser
import logging

class Config:

    configs = {}

    def __init__(self,cfg):
        home = expanduser("~")
        cfg = home + '/' + cfg
        logging.info("Reading config from : " + cfg)

        config = configparser.ConfigParser()
        config.read(cfg)
        for section in config.sections():
            options = config.options(section)
            for option in options:
                try:
                    self.configs[section + '_' + option] = config.get(section,option)
                except:
                    self.configs[section + '_' + option] = None

        print(self.configs)
