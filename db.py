from tinydb import TinyDB, Query
from decouple import config
from utils import sanitizeCommand
import psycopg2
from reserved_commands import reserved_commands

def init():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS command (
            id int NOT NULL,
            guild_id varchar(100) NOT NULL,
            command varchar(100) NOT NULL,
            value varchar(255) NOT NULL,
            CONSTRAINT command_pk PRIMARY KEY (id),
            CONSTRAINT command_guild_id_uk UNIQUE (guild_id, command)
        )''')
    cursor.execute('CREATE SEQUENCE IF NOT EXISTS command_id_seq OWNED BY command.id')
    cursor.execute('ALTER TABLE command ALTER COLUMN id SET DEFAULT nextval(\'command_id_seq\')')
    cursor.close()
    conn.commit()
    conn.close()

def connect():
    return psycopg2.connect(
        host=config('DB_HOST'),
        port=config('DB_PORT'),
        database=config('DB_NAME'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'))

def insert(guild_id, command, value):
    conn = connect()
    cursor = conn.cursor()
    command = sanitizeCommand(command)
    command = command.strip()
    if (command in reserved_commands):
        return 'Command not allowed'
    value = value.strip()
    result = get(guild_id, command)
    if (result != None):
        return 'Command already exists!'
    sql = F"INSERT INTO command (guild_id, command, value) VALUES ('{guild_id}', '{command}', '{value}')"
    try:
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        raise Exception(error)
    return 'New command added!'

def remove(guild_id, command):
    conn = connect()
    cursor = conn.cursor()
    command = sanitizeCommand(command)
    sql = F"DELETE FROM command WHERE guild_id = '{guild_id}' AND command = '{command}'"
    try:
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return 'No commands to remove'
    return 'Command removed!'

def get(guild_id, command):
    conn = connect()
    cursor = conn.cursor()
    command = sanitizeCommand(command)
    sql = F"SELECT value FROM command WHERE guild_id = '{guild_id}' AND command = '{command}'"
    cursor.execute(sql)
    res = cursor.fetchone()
    if (res == None):
        return None
    result = res[0]
    cursor.close()
    conn.close()
    return result