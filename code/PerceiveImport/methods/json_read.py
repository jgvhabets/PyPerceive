""" load and read a json file """

import json
from os import join

def read_json(path, filename):
    # open file, 'r' stands for read
    with open(join(path, filename), 'r') as f:
        json_object = json.loads(f.read())

    return json_object
    # output will be the dictionary stored in the json file

