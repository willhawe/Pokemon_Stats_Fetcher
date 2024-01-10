import requests
import sys
import sqlite3

POKEMON_API = "https://pokeapi.co/api/v2/pokemon/"
DB_FILE = "pokemon_stats.db"

def get_pokemon_details_from_api(pokemon_name):
    url = POKEMON_API + pokemon_name
    try:
        api_response = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Pokemon details")
        sys.exit(1)

    inbound_dict = {
        'id': api_response.get('id'),
        'name': api_response.get('name'),
        'height': api_response.get('height'),
        'weight': api_response.get('weight')
    }
    return inbound_dict

def create_table(cursor):
    command_create_table = """CREATE TABLE IF NOT EXISTS
    store(id INTEGER PRIMARY KEY, name TEXT, height INTEGER, weight INTEGER)"""
    cursor.execute(command_create_table)

def insert_into_table(cursor, pokemon_details):
    command_select = "SELECT * FROM store WHERE name = ?"
    cursor.execute(command_select, (pokemon_details['name'].lower(),))
    result = cursor.fetchone()

    if not result:
        command_insert = "INSERT INTO store (id, name, height, weight) VALUES (?, ?, ?, ?)"
        cursor.execute(command_insert, (pokemon_details['id'], pokemon_details['name'], pokemon_details['height'], pokemon_details['weight']))
        cursor.connection.commit()

def print_pokemon_details(result):
    if result:
        print("\n=== Pokemon Details ===")
        print(f"ID: {result[0]}")
        print(f"Name: {result[1].capitalize()}")
        print(f"Height: {result[2]}")
        print(f"Weight: {result[3]}")
        print("=======================")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <pokemon_name>")
        sys.exit(1)

    pokemon_name = sys.argv[1].lower()

    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        create_table(cursor)

        insert_into_table(cursor, get_pokemon_details_from_api(pokemon_name))

        command_select = "SELECT * FROM store WHERE name = ?"
        cursor.execute(command_select, (pokemon_name,))
        result = cursor.fetchone()                                                  
                                                                                    
        print_pokemon_details(result)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:                                                                       
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
