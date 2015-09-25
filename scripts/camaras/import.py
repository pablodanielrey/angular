import subprocess
import sys
import re,datetime,psycopg2,logging

import inject
sys.path.insert(0,'../../python')

from model.config import Config
from model.systems.camaras.camaras import Camaras



class Import:

    def __init__(self,config,camaras):
        self.camaras = camaras
        self.HOST="163.10.17.2"
        logging.debug('instanciando')

    def _getDatabase(self):
        host = '127.0.0.1'
        dbname = 'dcsys'
        user = 'dcsys'
        passw = 'dcsys'
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    def _getNumber(self,array):
        numbers = []
        for a in array:
            if a.isnumeric():
                numbers.append(a)
        if len(numbers) == 2:
            return float(numbers[0] + '.' + numbers[1])
        else:
            return float(numbers[0])

    def convertSize(self,sizeStr):

        numbersArray = re.split('[a-z,]+', sizeStr, flags=re.IGNORECASE)
        number = self._getNumber(numbersArray)
        unit = re.search('[gGmMkK]',sizeStr)
        if unit != None:
            unit = unit.group(0)
        if unit is None:
            return number
        elif unit.lower() == 'k':
            return number * 1024
        elif unit.lower() == 'm':
            return number * 1024 * 1024
        elif unit.lower() == 'g':
            return number * 1024 * 1024 * 1024
        else:
            return number


    def execute(self):

        # Ports are handled in ~/.ssh/config since we use OpenSSH
        source = '/gluster/camaras/archivo'

        # obtengo las camaras
        camaras = {
                    'camara1':'7d67a570-8151-430a-8423-a2f1b56d08c3',
                    'camara2':'3cdadbc0-35ad-4ac4-a1d2-8e8b6b3b1a73',
                    'camara3':'5e7da5d1-88a7-430a-8eb8-915e4d3d8f5d'
                  }

        # proceso los archivos
        command = "ls -sh " + source
        ssh = subprocess.Popen(["ssh", "%s" % self.HOST, command],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()

        try:
            con = self._getDatabase()
            self.camaras.deleteAllRecordings(con)
            con.commit()
            for r in result:
                r = r.decode('utf-8')
                if r.strip()[-4:] == '.mp4':
                    array = r.split()
                    rec = {}

                    rec['size'] = self.convertSize(array[0])

                    rec['file_name'] = array[1]
                    rec['fps'] = 15
                    rec['source'] = 'http://camaras.econo.unlp.edu.ar/' + rec['file_name']
                    rec['duration'] = '01:00:00'

                    arrayName = rec['file_name'].split('_')
                    start = datetime.datetime.strptime(arrayName[0] + " " + arrayName[1], "%Y-%m-%d %H-%M-%S")
                    start = start.replace(second=0,microsecond=0)
                    end = datetime.timedelta(hours=1) + start

                    rec['start'] = start
                    rec['rend'] = end

                    cameraName = arrayName[2].split('.')[0]
                    rec['camera_id'] = camaras[cameraName]

                    self.camaras.persistCamera(con,rec)
                con.commit()
        except Exception as e:
            logging.exception(e)
        finally:
            con.close()

def config_injector(binder):
    binder.bind(Config,Config('server-config.cfg'))

inject.configure(config_injector)
camaras = inject.instance(Camaras)
config = inject.instance(Config)
imp = Import(config,camaras)
imp.execute()
