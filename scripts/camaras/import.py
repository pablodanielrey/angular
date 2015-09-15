import subprocess
import sys
import re,datetime,psycopg2

import inject
sys.path.insert(0,'../../python')

from model.config import Config
from model.systems.camaras.camaras import Camaras

def config_injector(binder):
    binder.bind(Config,Config('server-config.cfg'))


class Import:

    def __init__(self,config,camaras):
        self.camaras = camaras
        self.serverConfig = config
        self.HOST="163.10.17.2"

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)


    def execute(self):

        # Ports are handled in ~/.ssh/config since we use OpenSSH
        source = '/gluster/camaras/archivo'

        # obtengo las camaras
        camara1Id = '7d67a570-8151-430a-8423-a2f1b56d08c3'
        camara2Id = '3cdadbc0-35ad-4ac4-a1d2-8e8b6b3b1a73'
        camara3Id = '5e7da5d1-88a7-430a-8eb8-915e4d3d8f5d'
        # proceso los archivos
        command = "ls -sh " + source
        ssh = subprocess.Popen(["ssh", "%s" % self.HOST, command],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()

        for r in result:
            r = r.decode('utf-8')
            if r.strip()[-4:] == '.mp4':
                array = r.split()
                size = array[0]
                file_name = array[1]
                fps = 15
                src = source + '/' + file_name
                duration = '01:00:00'

                arrayName = file_name.split('_')
                start = datetime.datetime.strptime(arrayName[0] + " " + arrayName[1], "%Y-%m-%d %H-%M-%S")
                start = start.replace(second=0,microsecond=0)
                end = datetime.timedelta(hours=1) + start

                camara = arrayName[2].split('.')[0]
                print(camara)
                '''
                    start =
                    end =
                    camera_id =
                '''



inject.configure(config_injector)
config = inject.instance(Config)
camaras = inject.instance(Camaras)
imp = Import(config,camaras)
imp.execute()
