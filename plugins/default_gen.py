from queue import Queue
from threading import Thread
import threading

from framework.logger import Log, Logger

# Object that signals shutdown
_shutdown = -1

log = Log(5)

class Generator(threading.Thread):
    def __init__(self, q_out, thread_id, name, config):
        threading.Thread.__init__(self)
        self.q_out = q_out
        self.thread_id = thread_id
        self.name = name
        self.message_count = 0

        # Config
        if 'logLevel' in config:
            self.log_level = config['logLevel']
        else:
            self.log_level = 5

        if 'showStage' in config:
            self.show_stage = config['showStage']
        else:
            self.show_stage = False

        log.set_level(int(self.log_level))

    def run(self):
        log.log_msg(Logger.INFO, self.name + ' started running')

        # Generate data
        self.generate()
        
        # Send the shutdown signal to next stage
        self.q_out.put(_shutdown)

        log.log_msg(Logger.INFO, self.name + ' finished running and generated ' + str(self.message_count) + ' messages')

    def generate(self):
        # Add logic to generate data and push output
        for i in range(100):
            self.q_out.put(i)
            self.message_count += 1