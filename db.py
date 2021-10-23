from tinydb import TinyDB, Query

db = TinyDB('database/db.json')

def init():
    if (db.all() != []):
        clearAll()
    db.insert({ 'command': '$hello', 'value': 'Hello!' })
    db.insert({ 'command': '$test', 'value': 'Why are you testing me?' })
    db.insert({ 'command': '$bomdia', 'value': 'Bom dia é o caralho' })

def insert(command, value):
    if (command.startswith('$') == False):
        command = '$' + command
    result = db.search(Query().command == command)
    if (result == []):
        db.insert({'command': command, 'value': value})
        return 'New command added!'
    else:
        return 'Command already exists'

def get(command):
    query = Query()
    results = db.search(query.command == command)
    if (results == []):
        raise Exception('Command not found')
    return results[0]['value']

def clearAll():
    db.truncate()
    db.all()