from checks import check_server, check_all_servers
from storage import export_csv, export_summary, save_servers

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
    return None


def filter_by_environment(servers, environment):
    return [server for server in servers if server['environment'] == environment]


def ask(prompt):
    # Keep asking until the answer is not empty
    while True:
        answer = input(prompt).strip()
        if answer:
            return answer
        print("This field can't be empty.")


def ask_name(prompt):
    # A server name must be one word, so it can be used with --check
    while True:
        name = ask(prompt)
        if ' ' not in name:
            return name
        print("The name can't contain spaces.")


def run_menu(servers, filename, verbose=False):
    first_time = True
    while True:
        # The pause is at the top so the 'continue' lines below don't skip it
        if not first_time:
            input("\nPress Enter to return to the menu...")
        first_time = False
        print()
        print("Server Inventory Tool")
        print("1. Show all servers")
        print("2. Check a server")
        print("3. Check all servers")
        print("4. Show all servers in environment")
        print("5. Add a new server")
        print("6. Remove a server")
        print("7. Export report (CSV and summary)")
        print("0. Quit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            print_servers(servers)
        elif choice == '2':
            print("Servers: " + ", ".join(server['name'] for server in servers))
            name = input("Server name: ")
            server = find_server(servers, name)
            if server is None:
                print(f"No server named {name}")
            else:
                check_server(server, verbose)
                save_servers(filename, servers)
                print_servers([server])
        elif choice == '3':
            check_all_servers(servers, verbose)
            save_servers(filename, servers)
            print_servers(servers)
        elif choice == '4':
            environment = input(f"Environment ({', '.join(VALID_ENVIRONMENTS)}): ")
            print_servers(filter_by_environment(servers, environment))
        elif choice == '5':
            name = ask_name("Server name: ")
            if find_server(servers, name) is not None:
                print(f"A server named {name} already exists.")
                continue
            address = ask("Server address: ")
            while True:
                environment = input(f"Environment ({', '.join(VALID_ENVIRONMENTS)}): ").strip()
                if environment in VALID_ENVIRONMENTS:
                    break
                print("Environment must be 'dev', 'test', or 'prod'.")
            role = ask("Role: ")
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
            print("Servers: " + ", ".join(server['name'] for server in servers))
            name = input("Server name: ")
            server = find_server(servers, name)
            if server is None:
                print(f"No server named {name}")
                continue
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
            summary_file = export_summary(servers)
            print(f"Servers exported to {report_file}.")
            print(f"Summary saved to {summary_file}.")
        elif choice == '0':
            break
        else:
            print("Invalid choice, try again.")
