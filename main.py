#mian.py
import argparse
import json
import sys
from core import Pipeline
from framework.logger import Log, Logger

log = Log(5)

if __name__ == "__main__":
    # Add arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
        description="PythonPluginPipeline", 
        epilog="Example Usages:\npython main.py" +
            " --input ./config/basic_config.json")
    parser.add_argument('--config', help="Config file path to configure the pipeline.", required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Get the config_path from args
    config_path = args.config

    # Read in config file
    f = open(config_path, 'r')
    config = json.load(f)

    # Initialize our pipeline
    pipeline = Pipeline(config)
    
    # Run the pipeline
    pipeline.run()