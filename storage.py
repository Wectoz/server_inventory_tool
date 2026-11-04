import json


def load_servers(filename):
    with open(filename) as file:
        return json.load(file)