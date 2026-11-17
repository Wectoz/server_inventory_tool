import json
import csv
from datetime import datetime
from pathlib import Path


def load_servers(filename):
    if not Path(filename).exists():
        return []
    with open(filename) as file:
        return json.load(file)


def save_servers(filename, servers):
    with open(filename, 'w') as file:
        json.dump(servers, file, indent=2)


def report_path(prefix, extension):
    # The date and time in the name means a new report never overwrites an old one
    Path('reports').mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    return 'reports/' + prefix + '_' + timestamp + extension


def export_csv(servers):
    filename = report_path('inventory', '.csv')
    # newline='' stops the csv module from adding empty lines between rows
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'address', 'environment', 'role', 'status', 'last_checked']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for server in servers:
            writer.writerow(server)
    return filename


def count_statuses(servers):
    counts = {'up': 0, 'down': 0, 'unknown': 0}
    for server in servers:
        counts[server['status']] += 1
    return counts


def export_summary(servers):
    filename = report_path('summary', '.txt')
    # Group the servers: first all of them, then one group per environment
    groups = {'all': servers}
    for server in servers:
        environment = server['environment']
        if environment not in groups:
            groups[environment] = []
        groups[environment].append(server)

    with open(filename, 'w') as file:
        file.write(f"{'':<10} {'UP':>5} {'DOWN':>5} {'UNKNOWN':>8} {'TOTAL':>6}\n")
        for label, group in groups.items():
            counts = count_statuses(group)
            file.write(f"{label:<10} {counts['up']:>5} {counts['down']:>5} {counts['unknown']:>8} {len(group):>6}\n")
    return filename