from os.path import expanduser
import configparser

class Config:

    configs = {}

    def __init__(self):
        home = expanduser("~")
        cfg = home + '/' + 'server-config.cfg'
        print("Reading config from : " + cfg)

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
