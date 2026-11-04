import subprocess

def ping(address):
    result = subprocess.run(["ping", "-c", "1", "-W", "2", address], capture_output=True)
    return result.returncode == 0