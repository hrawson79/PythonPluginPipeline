from queue import Queue
from threading import Thread
import threading

from framework.logger import Log, Logger

# Object that signals shutdown
_shutdown = -1

log = Log(5)

class Generator(threading.Thread):
    def __init__(self, q_out, threadID, name, counter):
        threading.Thread.__init__(self)
        self.q_out = q_out
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        log.LogMsg(Logger.INFO, 'Generator started running')
        # Generate data and put it on out_q
        for i in range(10):
            self.q_out.put(i)
        
        # Send the shutdown signal
        self.q_out.put(_shutdown)
        log.LogMsg(Logger.INFO, 'Generator finished running')