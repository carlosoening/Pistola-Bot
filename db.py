from tinydb import TinyDB, Query
import os

if not os.path.exists('database'):
    os.makedirs('database')

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

def remove(command):
    db.remove(Query().command == command)

def get(command): 
    results = db.search(Query().command == command)
    if (results == []):
        raise Exception('Command not found')
    return results[0]['value']

def clearAll():
    db.truncate()
    db.all()