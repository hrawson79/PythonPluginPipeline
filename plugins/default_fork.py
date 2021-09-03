from queue import Queue
from threading import Thread
import threading

from framework.logger import Log, Logger

# Object that signals shutdown
_shutdown = -1

log = Log(5)

class Fork(threading.Thread):
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

        self.showStage = False

        log.setLevel(int(self.logLevel))

    def run(self):
        log.LogMsg(Logger.INFO, self.name + ' started running')

        # Fork data
        self.fork()

        # Send shutdown the signal to next stages
        for q in self.q_out:
            q.put(_shutdown)
        
        log.LogMsg(Logger.INFO, self.name + ' finished running and forked ' + str(self.messageCount) + ' messages')

    def fork(self):
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
                for q in self.q_out:
                    q.put(data*2)
                self.q_in.task_done()
                self.messageCount += 1