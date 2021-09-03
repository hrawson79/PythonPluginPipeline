#core.py
import importlib
from queue import Queue
import numpy as np
import cv2
import time

from framework.logger import Log, Logger

log = Log(5)

class Pipeline:
    def __init__(self, config):
        self._q = {}
        self._plugins = []
        
        # Traverse the config and create the pipeline
        for p in config:
            if p['type'] == 'Generator':
                self.createGenerator(p)
            elif p['type'] == 'Processor':
                self.createProcessor(p)
            elif p['type'] == 'Writer':
                self.createWriter(p)
            elif p['type'] == 'Fork':
                self.createFork(p)

    def run(self):
        log.LogMsg(Logger.INFO, 'Starting pipeline')

        # Start all of the plugins
        for plugin in self._plugins:
            plugin.start()
        
        # Display each stage's current frame, if showStage is true
        while True:
            for plugin in self._plugins:
                if plugin.showStage:
                    cv2.imshow(plugin.name, plugin.currentFrame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

        # Wait until all tasks have completed
        for each in self._q:
            self._q[each].join()

        log.LogMsg(Logger.INFO, 'Ending pipeline')

    # Function to create a Generator type plugin
    def createGenerator(self, generator):
        topic = generator['outTopic']
        # Check if topic already added
        if topic in self._q:
            log.LogMsg(Logger.INFO, topic + ' topic already exists')
        else:
            log.LogMsg(Logger.INFO, 'Adding ' + topic + ' topic to _q')
            self._q[topic] = Queue()
        # Create a Generator plugin
        self._plugins.append(importlib.import_module(generator['plugin'],"plugins").Generator(
            self._q[topic], 1, generator['name'], generator['config']))

    # Function to create a Processor type plugin
    def createProcessor(self, processor):
        topic_in = processor['inTopic']
        # Check if input topic already added
        if topic_in in self._q:
            log.LogMsg(Logger.INFO, topic_in + ' topic already exists')
        else:
            log.LogMsg(Logger.INFO, 'Adding ' + topic_in + ' topic to _q')
            self._q[topic_in] = Queue()
        topic_out = processor['outTopic']

        # Check if output topic already added
        if topic_out in self._q:
            log.LogMsg(Logger.INFO, topic_out + ' topic already exists')
        else:
            log.LogMsg(Logger.INFO, 'Adding ' + topic_out + ' topic to _q')
            self._q[topic_out] = Queue()

        # Create a Processor plugin
        self._plugins.append(importlib.import_module(processor['plugin'],"plugins").Processor(
            self._q[topic_in], self._q[topic_out], 1, processor['name'], processor['config']))

    # Function to create a Writer type plugin
    def createWriter(self, writer):
        topic = writer['inTopic']
        # Check if topic already added
        if topic in self._q:
            log.LogMsg(Logger.INFO, topic + ' topic already exists')
        else:
            log.LogMsg(Logger.INFO, 'Adding ' + topic + ' topic to _q')
            self._q[topic] = Queue()

        # Create a Writer plugin
        self._plugins.append(importlib.import_module(writer['plugin'],"plugins").Writer(
            self._q[topic], 1, writer['name'], writer['config']))

    # Function to create a Fork type plugin
    def createFork(self, fork):
        topic_in = fork['inTopic']
        # Check if input topic already added
        if topic_in in self._q:
            log.LogMsg(Logger.INFO, topic_in + ' topic already exists')
        else:
            log.LogMsg(Logger.INFO, 'Adding ' + topic_in + ' topic to _q')
            self._q[topic_in] = Queue()

        out_topics = []
        for topic_out in fork['outTopic']:
            # Check if output topic already added
            if topic_out in self._q:
                log.LogMsg(Logger.INFO, topic_out + ' topic already exists')
            else:
                log.LogMsg(Logger.INFO, 'Adding ' + topic_out + ' topic to _q')
                self._q[topic_out] = Queue()
            # Add to out_topics list
            out_topics.append(self._q[topic_out])
                
        # Create a Processor plugin
        self._plugins.append(importlib.import_module(fork['plugin'],"plugins").Fork(
            self._q[topic_in], out_topics, 1, fork['name'], fork['config']))