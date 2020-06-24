from configparser import ConfigParser
from ast import literal_eval
import argparse
import os
from pathlib import Path

mappings = {}
endpoints = {}
configs = {}


def set_configs(config_file):
    config = ConfigParser()
    file_path = Path(os.path.dirname(__file__) + config_file)
    config.read(file_path)
    global mappings, endpoints, configs
    mappings = {key: infer_value_type(value) for key, value in config.items("MAPPINGS")}
    endpoints = {key: infer_value_type(value) for key, value in config.items("ENDPOINTS")}
    configs = {key: infer_value_type(value) for key, value in config.items("DEFAULT")}
    endpoints = argparse.Namespace(**endpoints)
    mappings = argparse.Namespace(**mappings)
    configs = argparse.Namespace(**configs)


def infer_value_type(string):
    try:
        parsed = literal_eval(string)
        return parsed
    except ValueError:
        return string
