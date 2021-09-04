from queue import Queue
from threading import Thread
import threading

from framework.logger import Log, Logger
from framework.configurator import *

# Object that signals shutdown
_shutdown = -1

log = Log(5)

class Fork(threading.Thread):
    def __init__(self, q_in, q_out, thread_id, name, config):
        threading.Thread.__init__(self)
        self.q_in = q_in
        self.q_out = q_out
        self.thread_id = thread_id
        self.name = name
        self.message_count = 0

        # Config
        self.log_level = load_config('logLevel', config, 5)
        self.show_stage = False

        log.set_level(int(self.log_level))

    def run(self):
        log.log_msg(Logger.INFO, self.name + ' started running')

        # Fork data
        self.fork()

        # Send shutdown the signal to next stages
        for q in self.q_out:
            q.put(_shutdown)
        
        log.log_msg(Logger.INFO, self.name + ' finished running and forked ' + str(self.message_count) + ' messages')

    def fork(self):
        while True:
            # Get data off of q_in
            data = self.q_in.get()

            # Check for shutdown signal
            if data is _shutdown:
                log.log_msg(Logger.INFO, self.name + ' received shutdown')
                self.q_in.task_done()
                break
            else:
                #log.log_msg(Logger.DEBUG, self.name + ' received ' + str(data) + ' to process')
                for q in self.q_out:
                    q.put(data)
                self.q_in.task_done()
                self.message_count += 1