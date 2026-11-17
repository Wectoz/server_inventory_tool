# Server Inventory Tool

A small command-line tool that keeps a list of servers in a JSON file, pings them to see if they answer, and exports the list as a CSV report.

Made as the final assignment in the course *Programmering med Python*.

## Getting started

```bash
git clone https://github.com/wectoz/server_inventory_tool.git
cd server_inventory_tool
python3 main.py
```

You need Python 3 and nothing else. `servers.json` comes with four example servers.

The checks use `ping -c 1 -W 2`, which works on Linux and WSL (tested on Ubuntu in WSL). They do not work on Windows without WSL, and may be unreliable on macOS.

## Menu mode

Run `python3 main.py` without flags:

```
Server Inventory Tool
1. Show all servers
2. Check a server
3. Check all servers
4. Show all servers in environment
5. Add a new server
6. Remove a server
7. Export report (CSV and summary)
0. Quit
```

Type a number and press Enter. After each option, press Enter again to get back to the menu.

- Options that ask for a server or an environment show what you can choose from.
- Checking shows the result as a table, with the new status and time.
- The environment must be `dev`, `test` or `prod`.
- Two servers can't have the same name.
- When you add a server, an empty answer or a name with spaces is not accepted. The program asks again until the value is valid.
- Removing a `prod` server asks you to type `yes` first.
- Every change is saved right away.

## CLI mode

With a flag, the program does one thing and exits.

| Command | What it does |
|---|---|
| `python3 main.py --help` | Shows all flags |
| `python3 main.py --list` | Lists all servers |
| `python3 main.py --list --environment prod` | Lists the servers in one environment |
| `python3 main.py --check web01` | Pings one server, saves and shows the result |
| `python3 main.py --check-all` | Pings all servers, saves and shows the results |
| `python3 main.py --export` | Creates a CSV report and a summary |
| `python3 main.py --check web01 --verbose` | Adds `--verbose` to any command to show more details |

```
$ python3 main.py --check-all
NAME       ADDRESS         ENVIRONMENT     ROLE            STATUS     LAST CHECKED
-----------------------------------------------------------------------------
web01      example.com     prod            webserver       up         2026-11-17 15:21
db01       127.0.0.1       prod            database        up         2026-11-17 15:21
test01     192.0.2.10      test            testserver      down       2026-11-17 15:21
dev01      localhost       dev             devserver       up         2026-11-17 15:21
```

`test01` is always `down`: its address is reserved for documentation and never answers. `example.com` can also show as `down` on networks that block ping.

### Exit codes

`--check` and `--check-all` exit with `0` if every checked server is up, and `1` if one is down or the name doesn't exist. A script can use this, for example to stop a deploy:

```bash
python3 main.py --check web01
echo $?
```

## Verbose mode

Add `--verbose` to see which data file is used and the exact `ping` command that runs for each check. It works with the other flags and with the menu.

```
$ python3 main.py --check dev01 --verbose
Using data file: servers.json
Running: ping -c 1 -W 2 localhost
NAME       ADDRESS         ENVIRONMENT     ROLE            STATUS     LAST CHECKED
-----------------------------------------------------------------------------
dev01      localhost       dev             devserver       up         2026-11-17 15:21
```

This is useful when a check gives a result you didn't expect, since you can copy the command and run it yourself.

## Data file

The program uses `servers.json` in the current folder. Set `INVENTORY_DATAFILE` to use another file:

```bash
INVENTORY_DATAFILE=my_servers.json python3 main.py --list
```

If the file doesn't exist, the program starts with an empty list and creates the file on the first save.

Each server looks like this:

```json
{
  "name": "web01",
  "address": "example.com",
  "environment": "prod",
  "role": "webserver",
  "status": "unknown",
  "last_checked": ""
}
```

`status` is `up`, `down` or `unknown` (new servers start as `unknown`). `last_checked` is `YYYY-MM-DD HH:MM`, or empty if the server has never been checked.

## Reports

`--export` or menu option 7 saves two files in `reports/`:

- a CSV file with every server, such as `reports/inventory_2026-11-17_1530.csv`
- a text summary, such as `reports/summary_2026-11-17_1530.txt`, that counts the servers by status, for all servers and for each environment

```
              UP  DOWN  UNKNOWN  TOTAL
all            3     1        0      4
prod           2     0        0      2
test           0     1        0      1
dev            1     0        0      1
```

The names include the date and time, so a new export doesn't overwrite an old one. The `reports/` folder is created when needed and is not tracked by Git.

## Files

| File | What it does |
|---|---|
| `main.py` | Starting point. Reads the flags, or starts the menu if there are none |
| `menu.py` | The text menu, and the functions that show, find and filter servers |
| `storage.py` | Loads and saves the JSON file, exports the CSV report and the summary |
| `checks.py` | Pings servers and updates their status |
| `servers.json` | The server data |
| `EXPLANATION.md` | Written explanation of the code (in Swedish) |

The menu and the flags use the same functions, so each piece of logic exists in one place.

## Names compared to the assignment

The assignment uses Swedish names. This project is written in English:

| Assignment | This project |
|---|---|
| `namn`, `adress`, `miljo`, `roll`, `senast_kontrollerad` | `name`, `address`, `environment`, `role`, `last_checked` |
| `servrar.json` | `servers.json` |
| `INVENTORY_DATAFIL` | `INVENTORY_DATAFILE` |
| `--lista`, `--miljo` | `--list`, `--environment` |
| `--kontrollera`, `--kontrollera-alla` | `--check`, `--check-all` |
| `meny.py`, `lagring.py`, `kontroller.py` | `menu.py`, `storage.py`, `checks.py` |
| `rapporter/inventering_...csv` | `reports/inventory_...csv` |
| `REDOGORELSE.md` | `EXPLANATION.md` |
| Roles `webbserver`, `databas`, `utvecklingsserver` | `webserver`, `database`, `devserver` |
