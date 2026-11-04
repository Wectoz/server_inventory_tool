import subprocess
from datetime import datetime


def ping(address):
    result = subprocess.run(["ping", "-c", "1", "-W", "2", address], capture_output=True)
    return result.returncode == 0


def check_server(server):
    answered = ping(server['address'])
    if answered:
        server['status'] = 'up'
    else:
        server['status'] = 'down'
    server['last_checked'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return answered
