#core.py
import importlib
from queue import Queue

from framework.logger import Log, Logger

log = Log(5)

class Pipeline:
    def __init__(self, config):
        self.q = [Queue(), Queue(), Queue()]
        self._plugins = [importlib.import_module('.default_gen',"plugins").Generator(self.q[0], 1, 'test', 1),
            importlib.import_module('.default_pro',"plugins").Processor(self.q[0], self.q[1], 2, 'test2', 1),
            importlib.import_module('.default_wri',"plugins").Writer(self.q[1], 3, 'test3', 1)]

    def run(self):
        log.LogMsg(Logger.INFO, 'Starting pipeline')

        for plugin in self._plugins:
            plugin.start()
        
        for each in self.q:
            each.join()
        #self.q[0].join()

        log.LogMsg(Logger.INFO, 'Ending pipeline')