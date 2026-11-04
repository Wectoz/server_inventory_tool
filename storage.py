import json
import csv
from datetime import datetime
from pathlib import Path


def load_servers(filename):
    with open(filename) as file:
        return json.load(file)


def save_servers(filename, servers):
    with open(filename, 'w') as file:
        json.dump(servers, file, indent=2)

def export_csv(servers):
    Path('reports').mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = 'reports/inventory_' + timestamp + '.csv'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'address', 'environment', 'role', 'status', 'last_checked']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for server in servers:
            writer.writerow(server)
    return filename