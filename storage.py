import json


def load_servers(filename):
    with open(filename) as file:
        return json.load(file)


def save_servers(filename, servers):
    with open(filename, 'w') as file:
        json.dump(servers, file, indent=2)
