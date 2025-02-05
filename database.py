import sqlite3

def initialize_database() -> None:
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()

    cursor.execute('''
        create table if not exists users (
            id,
            username,
            password,
            balance
        )
    ''')

    cursor.execute('''
        create table if not exists transactions(
            id,
            username,
            date,
            description 
        )
    ''')

    conn.commit()
    conn.close()

def execute_query(query: str, params: tuple = ()) -> None:
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_one(query: str, params: tuple = ()) -> tuple:
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result

def fetch_all(query: str, params: tuple = ()) -> list[tuple]:
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result
