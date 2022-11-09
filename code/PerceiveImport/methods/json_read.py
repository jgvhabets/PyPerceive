""" load and read a json file """

import json


# open file, 'r' stands for read
with open('matpart.json', 'r') as f:
    json_object = json.loads(f.read())

print(json_object)
# output will be the dictionary stored in the json file

