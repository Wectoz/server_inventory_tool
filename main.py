from storage import load_servers, save_servers, export_csv
from menu import run_menu, print_servers, find_server
from checks import check_server
import os
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Server Inventory Tool')
    parser.add_argument('--list', action='store_true', help='List all servers')
    parser.add_argument('--check-all', action='store_true', help='Check status of all servers')
    parser.add_argument('--export', action='store_true', help='Export server information to CSV')
    parser.add_argument('--check', metavar='NAME', help='Check one server by name')
    parser.add_argument('--environment', metavar='ENV', help='Only show servers in this environment (use with --list)')
    args = parser.parse_args()
    filename = os.environ.get('INVENTORY_DATAFILE', 'servers.json')
    servers = load_servers(filename)
    if args.list:
        if args.environment:
            filtered_servers = [s for s in servers if s['environment'] == args.environment]
            print_servers(filtered_servers)
        else:
            print_servers(servers)
    elif args.export:
        report_file = export_csv(servers)
        print(f"Exported server information to {report_file}")
    elif args.check:
        server = find_server(servers, args.check)
        if server is None:
            print(f"No server named {args.check}")
            sys.exit(1)
        else:
            answered = check_server(server)
            save_servers(filename, servers)
            print(f"{server['name']} is {server['status']}")
            if answered:
                sys.exit(0)
            else:
                sys.exit(1)
    elif args.check_all:
        all_up = True
        for server in servers:
            if not check_server(server):
                all_up = False
        save_servers(filename, servers)
        if all_up:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        run_menu(servers, filename)


if __name__ == "__main__":
    main()
