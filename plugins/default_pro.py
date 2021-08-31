from queue import Queue
from threading import Thread
import threading

from framework.logger import Log, Logger

# Object that signals shutdown
_shutdown = -1

log = Log(5)

class Processor(threading.Thread):
    def __init__(self, q_in, q_out, threadID, name, counter):
        threading.Thread.__init__(self)
        self.q_in = q_in
        self.q_out = q_out
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        log.LogMsg(Logger.INFO, 'Processor started running')

        while True:
            # Get data off of q_in
            data = self.q_in.get()

            # Check for shutdown signal
            if data is _shutdown:
                log.LogMsg(Logger.INFO, 'Processor received shutdown')
                self.q_in.task_done()
                break
            else:
                log.LogMsg(Logger.INFO, 'Processor received ' + str(data) + ' to process')
                self.q_out.put(data*2)
                self.q_in.task_done()

        # Send shutdown the signal
        self.q_out.put(_shutdown)        
        
        log.LogMsg(Logger.INFO, 'Processor finished running')