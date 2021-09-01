from queue import Queue
from threading import Thread
import threading

from framework.logger import Log, Logger

# Object that signals shutdown
_shutdown = -1

log = Log(5)

class Processor(threading.Thread):
    def __init__(self, q_in, q_out, threadID, name, config):
        threading.Thread.__init__(self)
        self.q_in = q_in
        self.q_out = q_out
        self.threadID = threadID
        self.name = name
        self.messageCount = 0

        # Config
        if 'logLevel' in config:
            self.logLevel = config['logLevel']
        else:
            self.logLevel = 5

        log.setLevel(int(self.logLevel))

    def run(self):
        log.LogMsg(Logger.INFO, self.name + ' started running')

        # Procces data
        self.process()

        # Send shutdown the signal to next stage
        self.q_out.put(_shutdown)        
        
        log.LogMsg(Logger.INFO, self.name + ' finished running and processed ' + str(self.messageCount) + ' messages')

    def process(self):
        # Add logic to process data and push output
        while True:
            # Get data off of q_in
            data = self.q_in.get()

            # Check for shutdown signal
            if data is _shutdown:
                log.LogMsg(Logger.INFO, self.name + ' received shutdown')
                self.q_in.task_done()
                break
            else:
                log.LogMsg(Logger.INFO, self.name + ' received ' + str(data) + ' to process')
                self.q_out.put(data * 2)
                self.q_in.task_done()
                self.messageCount += 1