import yaml

def load_conf(conf_file_location):
    with open(conf_file_location, "r") as f:
        data = yaml.safe_load_all(f.read())
    f.close()
    config = {}
    for config_item in data: 
        config.update(config_item)
    return config
