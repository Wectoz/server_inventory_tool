# Redogörelse

Projektet är skrivet på engelska, så fil- och funktionsnamnen nedan är de engelska. Tabellen sist i `README.md` visar vad de heter i uppgiften.

## 1. Tre konstruktioner i koden

**Villkor**, i `check_server` i `checks.py`:

```python
if answered:
    server['status'] = 'up'
else:
    server['status'] = 'down'
```

Efter `if` står ett uttryck som är sant eller falskt, och sedan ett kolon. De indragna raderna under `if` körs om det är sant, annars körs raderna under `else`. Här blir statusen `up` om servern svarade på ping och `down` om den inte gjorde det.

**Loop**, i `find_server` i `menu.py`:

```python
for server in servers:
    if server['name'] == name:
        return server
return None
```

`for` går igenom listan en server i taget. Om namnet stämmer returneras den servern direkt och loopen avbryts. Om ingen server har det namnet tar loopen slut och funktionen returnerar `None`.

**Funktion med parameter och `return`**, `ping` i `checks.py`:

```python
def ping(address):
    result = subprocess.run(["ping", "-c", "1", "-W", "2", address], capture_output=True)
    return result.returncode == 0
```

`def` skapar funktionen och `address` är en parameter som får sitt värde när funktionen anropas, till exempel `ping('localhost')`. Funktionen kör kommandot `ping` och `return` skickar tillbaka `True` om exitkoden var 0, alltså om servern svarade, och annars `False`.

## 2. Varför en lista med dictionaries

En server har flera egenskaper med namn, och i en dictionary kan jag hämta dem med till exempel `server['status']`, så det syns i koden vad jag menar. Servrarna är flera och jag vill ofta gå igenom alla, som i `print_servers` i `menu.py`, och då passar en lista. Det är också samma form som JSON-filen har, så `load_servers` i `storage.py` får rätt struktur direkt.

Alla sex värden i en server är strängar. `status` får bara vara `up`, `down` eller `unknown`, och `last_checked` är en tom sträng tills servern har kontrollerats.

## 3. JSON för data, CSV för rapporten

JSON-filen är till för programmet. Den behåller listan med dictionaries precis som den ser ut i Python, så `load_servers` och `save_servers` i `storage.py` behöver bara en rad var för att läsa och skriva.

CSV-rapporten är till för människor. Den är en tabell med en rubrikrad och en rad per server och går att öppna i Excel. Den skapas av `export_csv` i `storage.py`. JSON-filen skrivs över vid varje ändring, men varje rapport får ett eget filnamn med datum och tid.

## 4. Moduler och funktioner

- **`main.py`** är startpunkten. `main()` läser flaggorna och miljövariabeln, laddar servrarna och startar antingen menyn eller gör det flaggan säger.
- **`menu.py`** har textmenyn i `run_menu` och funktionerna som visar och hittar servrar: `print_servers`, `find_server` och `filter_by_environment`.
- **`storage.py`** sköter filerna: `load_servers`, `save_servers` och `export_csv`.
- **`checks.py`** sköter kontrollerna: `ping`, `check_server` och `check_all_servers`.

Menyn och kommandoraden använder samma funktioner. Till exempel anropar både menyval 3 i `run_menu` och `--check-all` i `main()` funktionen `check_all_servers`.

## 5. Moduler från standardbiblioteket

| Modul | Används i | Till vad |
|---|---|---|
| `json` | `load_servers`, `save_servers` | Läsa och spara datafilen |
| `csv` | `export_csv` | Skriva rapporten med rubrikrad |
| `os` | `main()` | Läsa miljövariabeln `INVENTORY_DATAFILE` |
| `pathlib` | `load_servers`, `export_csv` | Kolla om datafilen finns och skapa katalogen `reports/` |
| `datetime` | `check_server`, `export_csv` | Tiden för senaste kontroll och datum i rapportens filnamn |
| `subprocess` | `ping` | Köra kommandot `ping` |
| `argparse` | `main()` | Läsa flaggorna och skapa `--help` |
| `sys` | `main()` | Avsluta med exitkod 0 eller 1 |

## 6. Tre exempel på god praxis

1. **Samma logik finns bara på ett ställe.** Kontrollen av en server är skriven en gång, i `check_server` i `checks.py`, och används av både menyn och `--check`. Ska något ändras behöver jag bara ändra där.
2. **Kommandot till `subprocess.run()` är en lista.** I `ping` i `checks.py` skickas adressen som ett eget element i listan. Adressen skrivs in av användaren, och på det här sättet kan den aldrig köras som ett eget kommando.
3. **Filnamnet är inte hårdkodat i funktionerna.** `main()` läser det en gång och skickar det som parameter till `load_servers`, `save_servers` och `run_menu`. Då fungerar samma kod med vilken datafil som helst.

## 7. Källor och hjälpmedel

Jag har använt presentationer och tidigare uppgifter i kursen för att utveckla koden till detta projekt.

Jag har använt AI-verktyget Claude (Claude Code i VS Code) till att:

- göra en checklista av uppgiften
- förklara felmeddelanden och begrepp som indentering, `argparse` och exitkoder
- hjälpa mig att felsöka delar av koden: `print_servers`, `find_server`, `filter_by_environment` och första versionen av menyn i `menu.py`, `check_all_servers` och indenteringen i `check_server` i `checks.py`, filnamnet för rapporten i `storage.py` samt hanteringen av `--check` och `--environment` i `main.py`
- testa programmet mot kraven
- skriva ett första utkast till `README.md`
- fomrmatera `EXPLANATION.md` så det blev tydligt
