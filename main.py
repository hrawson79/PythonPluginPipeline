#mian.py
import json
import sys
from core import Pipeline
from framework.logger import Log, Logger

log = Log(5)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        log.LogMsg(Logger.ERROR, '-c flag must be set to supply config file path')
        sys.exit()
    if not args[0] == '-c':
        log.LogMsg(Logger.ERROR, '-c flag must be set to supply config file path')
        sys.exit()
    else:
        if len(args) < 2:
            log.LogMsg(Logger.ERROR, 'No config file given')
            sys.exit()
        else:
            config_path = args[1]
            log.LogMsg(Logger.INFO, 'Config file set to ' + config_path)
    
    # Read in config file
    f = open(config_path, 'r')
    config = json.load(f)
    # Initialize our pipeline
    pipeline = Pipeline(config)
    # Run the pipeline
    pipeline.run()