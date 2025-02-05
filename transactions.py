from database import execute_query, fetch_all
from datetime import datetime

def add_transaction(username: str, description: str) -> None:
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_query('INSERT INTO transactions (username, date, description) VALUES (?, ?, ?)', (username, date, description))

def get_transactions(username: str) -> list:
    transactions = fetch_all('SELECT date, description FROM transactions WHERE username = ?', (username,))
    return [f"{transaction[0]}: {transaction[1]}" for transaction in transactions]


