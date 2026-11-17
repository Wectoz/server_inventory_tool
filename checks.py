import subprocess
from datetime import datetime


def ping(address, verbose=False):
    # -c 1: send one ping. -W 2: wait at most 2 seconds for an answer
    command = ["ping", "-c", "1", "-W", "2", address]
    if verbose:
        print("Running: " + " ".join(command))
    result = subprocess.run(command, capture_output=True)
    # Exit code 0 means the server answered
    return result.returncode == 0


def check_server(server, verbose=False):
    answered = ping(server['address'], verbose)
    if answered:
        server['status'] = 'up'
    else:
        server['status'] = 'down'
    server['last_checked'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return answered


def check_all_servers(servers, verbose=False):
    # Returns True only if every server answered
    all_up = True
    for server in servers:
        if not check_server(server, verbose):
            all_up = False
    return all_up
