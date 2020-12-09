import csv
import os
from pathlib import Path

ROOT_DIR = Path(__file__).absolute().parent.parent
DEFAULT_INPUT_COORDS = ROOT_DIR / 'input/coords.csv'
DEFAULT_INPUT_VECTORS = ROOT_DIR / 'input/vectors.csv'
DEFAULT_OUTPUT_DIR = ROOT_DIR / 'output'


def read_file_as_list(file_name, delimiter=','):
    with open(file_name, 'r') as read_obj:
        dict_reader = csv.DictReader(read_obj)
        list_of_dict = list(dict_reader)
        return list_of_dict


def extract_int_property(property, coords):
    return [int(entry[property]) for entry in coords]


def extract_str_property(property, coords):
    return [str(entry[property]) for entry in coords]


def create_parent_dir(dir):
    os.makedirs(os.path.dirname(dir), exist_ok=True)
