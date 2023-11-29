import os, yaml
import yaml 

class Env: 
    def __init__(self, conf_file_location):

        with open(conf_file_location, "r") as f:
            config_file = f.read()

        data = yaml.safe_load_all(config_file)

        config = {}

        for config_item in data: 
            config.update(config_item)

        self.config = config

