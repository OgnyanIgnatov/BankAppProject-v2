import unittest
import sqlite3
from unittest.mock import patch, MagicMock
from user import register_user, log_in, get_balance, update_balance
from transactions import add_transaction, get_transactions
from database import initialize_database, execute_query
from app import start_gui

class TestUser(unittest.TestCase):
    def setUp(self):
        initialize_database()
        execute_query("DELETE FROM users")
        execute_query("DELETE FROM transactions")

    @patch('user.execute_query')  
    @patch('user.hash_password') 
    def test_register_user(self, mock_hash_password, mock_execute_query):
        username = "test_user"
        password = "password123"

        # Мокваме hash_password да върне фиксиран хеш
        mock_hash_password.return_value = "hashed_password"

        # Мокваме execute_query да не хвърля грешка (т.е. да няма дублиране на потребители)
        mock_execute_query.return_value = None

        result = register_user(username, password)

        self.assertEqual(result, "Registration successful")

    @patch('user.execute_query')
    def test_register_user_duplicate_username(self, mock_execute_query):
        username = "test_user"
        password = "password123"

        mock_execute_query.side_effect = sqlite3.IntegrityError("Username already exists.")

        with self.assertRaises(ValueError):
            register_user(username, password)

    def test_log_in(self):
        register_user("test_user", "password123")
        self.assertTrue(log_in("test_user", "password123"))
        self.assertFalse(log_in("test_user", "wrong_password"))

    def test_update_balance(self):
        register_user("test_user", "password123")
        update_balance("test_user", 100.0)
        self.assertEqual(get_balance("test_user"), 100.0)

    def test_add_money(self):
        register_user("test_user", "password123")
        update_balance("test_user", 100.0)
        self.assertEqual(get_balance("test_user"), 100.0)
        update_balance("test_user", 50.0)
        self.assertEqual(get_balance("test_user"), 50.0)

    def test_withdraw_money(self):
        register_user("test_user", "password123")
        update_balance("test_user", 100.0)
        self.assertEqual(get_balance("test_user"), 100.0)
        update_balance("test_user", -50.0)
        self.assertEqual(get_balance("test_user"), -50.0)

class TestTransactions(unittest.TestCase):
    def setUp(self):
        initialize_database()
        execute_query("DELETE FROM users")
        execute_query("DELETE FROM transactions")
        register_user("test_user", "password123")

    def test_add_transaction(self):
        add_transaction("test_user", "Added 50 to balance.")
        transactions = get_transactions("test_user")
        self.assertEqual(len(transactions), 1)

    def test_get_transactions(self):
        add_transaction("test_user", "Added 50 to balance.")
        add_transaction("test_user", "Withdrew 20 from balance.")
        transactions = get_transactions("test_user")
        self.assertEqual(len(transactions), 2)

    def test_no_transactions(self):
        transactions = get_transactions("test_user")
        self.assertEqual(len(transactions), 0)

class TestApp(unittest.TestCase):
    @patch("tkinter.Tk")
    def test_start_gui(self, mock_tk):
        import app
        app.start_gui()
        self.assertTrue(mock_tk.called)

    @patch("tkinter.Toplevel")
    def test_login_user_gui(self, mock_toplevel):
        from app import login_user_gui
        mock_root = MagicMock()
        login_user_gui(mock_root)
        self.assertTrue(mock_toplevel.called)

    @patch("tkinter.Toplevel")
    def test_register_user_gui(self, mock_toplevel):
        from app import register_user_gui
        mock_root = MagicMock()
        register_user_gui(mock_root)
        self.assertTrue(mock_toplevel.called)

if __name__ == "__main__":
    unittest.main()
