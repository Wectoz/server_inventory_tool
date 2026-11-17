import subprocess
from datetime import datetime


def ping(address):
    # -c 1: send one ping. -W 2: wait at most 2 seconds for an answer
    result = subprocess.run(["ping", "-c", "1", "-W", "2", address], capture_output=True)
    # Exit code 0 means the server answered
    return result.returncode == 0


def check_server(server):
    answered = ping(server['address'])
    if answered:
        server['status'] = 'up'
    else:
        server['status'] = 'down'
    server['last_checked'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return answered


def check_all_servers(servers):
    # Returns True only if every server answered
    all_up = True
    for server in servers:
        if not check_server(server):
            all_up = False
    return all_up
