from queue import Queue
from threading import Thread
import threading

from framework.logger import Log, Logger

# Object that signals shutdown
_shutdown = -1

log = Log(5)

class Generator(threading.Thread):
    def __init__(self, q_out, threadID, name, config):
        threading.Thread.__init__(self)
        self.q_out = q_out
        self.threadID = threadID
        self.name = name
        self.messageCount = 0

        # Config
        if 'logLevel' in config:
            self.logLevel = config['logLevel']
        else:
            self.logLevel = 5

        if 'showStage' in config:
            self.showStage = config['showStage']
        else:
            self.showStage = False

        log.setLevel(int(self.logLevel))

    def run(self):
        log.LogMsg(Logger.INFO, self.name + ' started running')

        # Generate data
        self.generate()
        
        # Send the shutdown signal to next stage
        self.q_out.put(_shutdown)

        log.LogMsg(Logger.INFO, self.name + ' finished running and generated ' + str(self.messageCount) + ' messages')

    def generate(self):
        # Add logic to generate data and push output
        for i in range(100):
            self.q_out.put(i)
            self.messageCount += 1