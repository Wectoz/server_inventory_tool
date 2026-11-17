import os
import argparse
import sys
from storage import load_servers, save_servers, export_csv, export_summary
from menu import run_menu, print_servers, find_server, filter_by_environment
from checks import check_server, check_all_servers


def main():
    parser = argparse.ArgumentParser(description='Server Inventory Tool')
    parser.add_argument('--list', action='store_true', help='List all servers')
    parser.add_argument('--check-all', action='store_true', help='Check status of all servers')
    parser.add_argument('--export', action='store_true', help='Export a CSV report and a summary')
    parser.add_argument('--check', metavar='NAME', help='Check one server by name')
    parser.add_argument('--environment', metavar='ENV', help='Only show servers in this environment (use with --list)')
    parser.add_argument('--verbose', action='store_true', help='Show more details, such as the data file and the ping command')
    args = parser.parse_args()
    filename = os.environ.get('INVENTORY_DATAFILE', 'servers.json')
    if args.verbose:
        print(f"Using data file: {filename}")
    servers = load_servers(filename)

    # Exit code 0 = OK, 1 = a server is down or was not found
    if args.list:
        if args.environment:
            print_servers(filter_by_environment(servers, args.environment))
        else:
            print_servers(servers)
    elif args.export:
        report_file = export_csv(servers)
        summary_file = export_summary(servers)
        print(f"Exported server information to {report_file}")
        print(f"Summary saved to {summary_file}")
    elif args.check:
        server = find_server(servers, args.check)
        if server is None:
            print(f"No server named {args.check}")
            sys.exit(1)
        else:
            answered = check_server(server, args.verbose)
            save_servers(filename, servers)
            print_servers([server])
            if answered:
                sys.exit(0)
            else:
                sys.exit(1)
    elif args.check_all:
        all_up = check_all_servers(servers, args.verbose)
        save_servers(filename, servers)
        print_servers(servers)
        if all_up:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        run_menu(servers, filename, args.verbose)


if __name__ == "__main__":
    main()
