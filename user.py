import hashlib
import sqlite3
from transactions import add_transaction
from database import execute_query, fetch_one, fetch_all

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str) -> str:
    hashed_password = hash_password(password)
    try:
        execute_query('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        return "Registration successful"
    except sqlite3.IntegrityError:
        raise ValueError("Username already exists.")
    
def log_in(username: str, password: str) -> bool:
    hashed_password = hash_password(password)
    user = fetch_one('SELECT username, password FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    return user is not None

def get_balance(username: str) -> float:
    result = fetch_one('SELECT balance FROM users WHERE username = ?', (username,))
    return result[0] if result else 0.0

def update_balance(username: str, new_balance: float) -> None:
    execute_query('UPDATE users SET balance = ? WHERE username = ?', (new_balance, username))

def transfer_money(from_username: str, to_username: str, amount: float) -> None:
    if from_username == to_username:
        raise ValueError("You cannot transfer money to yourself.")

    from_balance = get_balance(from_username)
    if from_balance < amount:
        raise ValueError("Insufficient funds.")

    to_balance = get_balance(to_username)

    new_from_balance = from_balance - amount
    new_to_balance = to_balance + amount

    update_balance(from_username, new_from_balance)
    update_balance(to_username, new_to_balance)

    add_transaction(from_username, f"Transferred {amount} to {to_username}")
    add_transaction(to_username, f"Received {amount} from {from_username}")
