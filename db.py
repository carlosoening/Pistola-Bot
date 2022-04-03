from tinydb import TinyDB, Query
import os
from utils import sanitizeCommand

if not os.path.exists('database'):
    os.makedirs('database')

db = TinyDB('database/db.json')

def init():
    insert('$hello', 'Hello!')
    insert('$test', 'Why are you testing me?')
    insert('$bomdia', 'Bom dia é o caralho')

def insert(command, value):
    command = sanitizeCommand(command)
    result = db.search(Query().command == command)
    if (result == []):
        db.insert({'command': command, 'value': value})
        return 'New command added!'
    else:
        return 'Command already exists'

def remove(command):
    command = sanitizeCommand(command)
    result = db.search(Query().command == command)
    if (result == []):
        return 'No commands to remove'
    db.remove(Query().command == command)
    return 'Command removed!'

def get(command): 
    results = db.search(Query().command == command)
    if (results == []):
        raise Exception('Command not found')
    return results[0]['value']

def clearAll():
    db.truncate()
    db.all()