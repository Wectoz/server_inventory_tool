from checks import check_server, check_all_servers
from storage import export_csv, save_servers

VALID_ENVIRONMENTS = ['dev', 'test', 'prod']


def print_servers(servers):
    print(f'{"NAME":<10} {"ADDRESS":<15} {"ENVIRONMENT":<15} {"ROLE":<15} {"STATUS":<10} {"LAST CHECKED":<5}')
    print('-' * 77)
    for server in servers:
        print(f"{server['name']:<10} {server['address']:<15} {server['environment']:<15} {server['role']:<15} {server['status']:<10} {server['last_checked']:<10}")


def find_server(servers, name):
    for server in servers:
        if server['name'] == name:
            return server
    # No server had that name
    return None


def filter_by_environment(servers, environment):
    return [server for server in servers if server['environment'] == environment]


def run_menu(servers, filename):
    while True:
        print()
        print("Server Inventory Tool")
        print("1. Show all servers")
        print("2. Check a server")
        print("3. Check all servers")
        print("4. Show all servers in environment")
        print("5. Add a new server")
        print("6. Remove a server")
        print("7. Export servers to CSV")
        print("0. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print_servers(servers)
        elif choice == '2':
            name = input("Server name: ")
            server = find_server(servers, name)
            if server is None:
                print(f"No server named {name}")
            else:
                check_server(server)
                save_servers(filename, servers)
                print(f"{server['name']} is {server['status']}")
        elif choice == '3':
            check_all_servers(servers)
            save_servers(filename, servers)
            print("All servers checked.")
        elif choice == '4':
            environment = input("Environment: ")
            print_servers(filter_by_environment(servers, environment))
        elif choice == '5':
            name = input("Server name: ")
            if find_server(servers, name) is not None:
                print(f"A server named {name} already exists.")
                # Skip the rest and show the menu again
                continue
            address = input("Server address: ")
            # Keep asking until the environment is valid
            while True:
                environment = input("Environment: ")
                if environment in VALID_ENVIRONMENTS:
                    break
                print("Environment must be 'dev', 'test', or 'prod'.")
            role = input("Role: ")
            new_server = {
                'name': name,
                'address': address,
                'environment': environment,
                'role': role,
                'status': 'unknown',
                'last_checked': ''
            }
            servers.append(new_server)
            save_servers(filename, servers)
            print(f"Server {name} added.")
        elif choice == '6':
            name = input("Server name: ")
            server = find_server(servers, name)
            if server is None:
                print(f"No server named {name}")
                continue
            # Production servers need an extra confirmation
            if server['environment'] == 'prod':
                confirmation = input(f"Are you sure you want to remove the production server {name}? (yes/no): ")
                if confirmation != 'yes':
                    print(f"Server {name} was not removed.")
                    continue
            servers.remove(server)
            save_servers(filename, servers)
            print(f"Server {name} removed.")
        elif choice == '7':
            report_file = export_csv(servers)
            print(f"Servers exported to {report_file}.")
        elif choice == '0':
            break
        else:
            print("Invalid choice, try again.")
