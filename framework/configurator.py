#configurator.py
def load_config(name, config, default):
    if name in config:
        return config[name]
    else:
        return default