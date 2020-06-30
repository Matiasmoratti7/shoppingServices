from configparser import ConfigParser
from ast import literal_eval
import argparse
import os
from pathlib import Path

configs = {}


def set_configs(config_file):
    config = ConfigParser()
    file_path = Path(os.path.dirname(__file__) + config_file)
    config.read(file_path)
    global configs
    args = {key: infer_value_type(value) for key, value in config.items("DEFAULT")}
    configs = argparse.Namespace(**args)


def infer_value_type(string):
    try:
        parsed = literal_eval(string)
        return parsed
    except ValueError:
        return string
