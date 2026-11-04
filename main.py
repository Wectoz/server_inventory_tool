from storage import load_servers
servers = load_servers('servers.json')
print(f'{"NAME":<10} {"ADDRESS":<15} {"ENVIRONMENT":<15} {"ROLE":<15} {"STATUS":<10} {"LAST CHECKED":<5}')
print(f'-----------------------------------------------------------------------------')
for server in servers:
    print(f"{server['name']:<10} {server['address']:<15} {server['environment']:<15} {server['role']:<15} {server['status']:<10} {server['last_checked']:<5} {server['last_checked']:<10}")