
import importlib
import inspect
from os import listdir
from os.path import isfile, join

class Context:
    """
        Representa la clase base de todos los contextos.
        Implementa métodos generales para uso en todos los contextos.
    """

    def _getDaos(self, entity):
        """
            obtengo las clases que se encuentran dentro del paquete .dao. relativo al paquete raiz de la entidad
        """
        pname = entity.__module__[0:entity.__module__.rfind('.')]
        mtoi = pname + '.dao'
        module = importlib.import_module(mtoi)
        root = module.__path__[0]

        files = [ f for f in listdir(root) if isfile(join(root,f)) ]
        modules = [importlib.import_module(mtoi + '.' + f.replace('.py','')) for f in files]

        clss = []
        for module in modules:
            for (name, clazz) in inspect.getmembers(module, inspect.isclass):
                clss.append(clazz)
        return clss

    def dao(self, entity):
        """
            Retorna el primer DAO que retorne True cuando se llama al método select
        """
        clazzes = self._getDaos(entity)
        for c in clazzes:
            if hasattr(c, '_select') and c._select(self):
                return c
        raise Error('No se encuentra dao correcto')


class SqlContext(Context):
    """
        Contexto de referencia general usado por los daos que acceden a bases SQL.
    """

    def __init__(self, con):
        self.con = con


class DAO:
    @classmethod
    def _select(cls, ctx):
        """
            Retorna True cuando el DAO puede trabajar con el contexto indicado
        """
        raise NotImplementedError()
