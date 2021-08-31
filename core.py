#core.py
import importlib
from queue import Queue

from framework.logger import Log, Logger

log = Log(5)

class Pipeline:
    def __init__(self, config):
        self._q = {}
        self._plugins = []

        for i in config:
            print(i)
        
        for p in config:
            if p['type'] == 'Generator':
                topic = p['outTopic']
                # Check if topic already added
                if topic in self._q:
                    log.LogMsg(Logger.INFO, topic + ' topic already exists')
                else:
                    log.LogMsg(Logger.INFO, 'Adding ' + topic + ' topic to _q')
                    self._q[topic] = Queue()
                # Create a Generator plugin
                self._plugins.append(importlib.import_module(p['plugin'],"plugins").Generator(self._q[topic], 1, p['name'], 1))
            elif p['type'] == 'Processor':
                topic_in = p['inTopic']
                # Check if topic already added
                if topic_in in self._q:
                    log.LogMsg(Logger.INFO, topic_in + ' topic already exists')
                else:
                    log.LogMsg(Logger.INFO, 'Adding ' + topic_in + ' topic to _q')
                    self._q[topic_in] = Queue()
                topic_out = p['outTopic']
                # Check if topic already added
                if topic_out in self._q:
                    log.LogMsg(Logger.INFO, topic_out + ' topic already exists')
                else:
                    log.LogMsg(Logger.INFO, 'Adding ' + topic_out + ' topic to _q')
                    self._q[topic_out] = Queue()                
                # Create a Processor plugin
                self._plugins.append(importlib.import_module(p['plugin'],"plugins").Processor(self._q[topic_in], self._q[topic_out], 1, p['name'], 1))
            elif p['type'] == 'Writer':
                topic = p['inTopic']
                # Check if topic already added
                if topic in self._q:
                    log.LogMsg(Logger.INFO, topic + ' topic already exists')
                else:
                    log.LogMsg(Logger.INFO, 'Adding ' + topic + ' topic to _q')
                    self._q[topic] = Queue()
                # Create a Writer plugin
                self._plugins.append(importlib.import_module(p['plugin'],"plugins").Writer(self._q[topic], 1, p['name'], 1))

    def run(self):
        log.LogMsg(Logger.INFO, 'Starting pipeline')

        # Start all of the plugins
        for plugin in self._plugins:
            plugin.start()
        
        # Wait until all tasks have completed
        for each in self._q:
            self._q[each].join()

        log.LogMsg(Logger.INFO, 'Ending pipeline')