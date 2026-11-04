from storage import load_servers
from menu import run_menu


def main():
    filename = 'servers.json'
    servers = load_servers(filename)
    run_menu(servers, filename)


if __name__ == "__main__":
    main()
