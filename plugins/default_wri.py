from queue import Queue
from threading import Thread
import threading

from framework.logger import Log, Logger

# Object that signals shutdown
_shutdown = -1

log = Log(5)

class Writer(threading.Thread):
    def __init__(self, q_in, threadID, name, config):
        threading.Thread.__init__(self)
        self.q_in = q_in
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
        
        # Write data
        self.write()

        log.LogMsg(Logger.INFO, self.name + ' finished running and wrote ' + str(self.messageCount) + ' messages')

    def write(self):
        # Add logic to write data to file here
        while True:
            # Get data off of q_in
            data = self.q_in.get()

            # Check for shutdown signal
            if data is _shutdown:
                log.LogMsg(Logger.INFO, self.name + ' received shutdown')
                self.q_in.task_done()
                break
            else:
                #log.LogMsg(Logger.DEBUG, self.name + ' received ' + str(data) + ' to process')
                self.q_in.task_done()
                self.messageCount += 1