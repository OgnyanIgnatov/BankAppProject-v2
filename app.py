import tkinter as tk
from tkinter import messagebox
from user import register_user, log_in, get_balance, update_balance, transfer_money
from transactions import add_transaction, get_transactions
from database import initialize_database

initialize_database()

button_style = {
        "font": ("Georgia", 8, "bold"),
        "bg":"white"
    }


def register_user_gui(parent) -> None:
    reg_window = tk.Toplevel(parent)
    reg_window.configure(bg="lightblue")
    reg_window.title("Register")
    tk.Label(reg_window, text="Username:", bg="lightblue", font=("Georgia", 10, "bold")).pack()
    username_entry = tk.Entry(reg_window)
    username_entry.pack()
    tk.Label(reg_window, text="Password:", bg="lightblue", font=("Georgia", 10, "bold")).pack()
    password_entry = tk.Entry(reg_window, show="*")
    password_entry.pack()

    def submit_registration() -> None:
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            try:
                register_user(username, password)
                messagebox.showinfo("Success", "Registration Successful!")
                reg_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Username already exists.")
        else:
            messagebox.showerror("Error", "Please fill all fields.")

    tk.Button(reg_window, text="Register", command=submit_registration, **button_style).pack(pady=10, ipadx=5, ipady=5)


def login_user_gui(parent) -> None:

    login_window = tk.Toplevel(parent)
    login_window.configure(bg="lightblue")
    login_window.title("Login")
    tk.Label(login_window, text="Username:", bg="lightblue", font=("Georgia", 10, "bold")).pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()
    tk.Label(login_window, text="Password:", bg="lightblue", font=("Georgia", 10, "bold")).pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def submit_login() -> None:
        username = username_entry.get()
        password = password_entry.get()
        if log_in(username, password):
            messagebox.showinfo("Success", "Login Successful!")
            login_window.destroy()
            show_user_dashboard(parent, username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    tk.Button(login_window, text="Login", command=submit_login, **button_style).pack(pady=10, ipadx=5, ipady=5)


def show_user_dashboard(parent, username: str) -> None:
    dashboard = tk.Toplevel(parent)
    dashboard.title(f"Welcome, {username}")
    dashboard.configure(bg="lightblue")  
    tk.Label(dashboard, text=f"Welcome, {username}!", bg="lightblue", font=("Georgia", 16, "bold")).pack()

    def show_balance() -> None:
        balance = get_balance(username)
        messagebox.showinfo("Balance", f"Your current balance is: {balance}")

    def add_money() -> None:
        add_window = tk.Toplevel(dashboard)
        add_window.title("Add Money")
        add_window.configure(bg="lightblue")  
        tk.Label(add_window, text="Amount:", font=("Georgia", 10, "bold"), bg="lightblue").pack()
        amount_entry = tk.Entry(add_window)
        amount_entry.pack()

        def submit_add() -> None:
            amount = float(amount_entry.get())
            balance = get_balance(username)
            update_balance(username, balance + amount)
            add_transaction(username, f"Added {amount} to balance.")
            messagebox.showinfo("Success", f"Added {amount} to balance.")
            add_window.destroy()

        tk.Button(add_window, text="Add", command=submit_add, **button_style, width=10, height=2).pack(pady=10)

    def withdraw_money() -> None:
        withdraw_window = tk.Toplevel(dashboard)
        withdraw_window.title("Withdraw Money")
        withdraw_window.configure(bg="lightblue") 
        tk.Label(withdraw_window, text="Amount:", bg="lightblue", font=("Georgia", 10, "bold")).pack()
        amount_entry = tk.Entry(withdraw_window)
        amount_entry.pack()

        def submit_withdraw() -> None:
            amount = float(amount_entry.get())
            balance = get_balance(username)
            if amount > balance:
                messagebox.showerror("Error", "Insufficient funds.")
            else:
                update_balance(username, balance - amount)
                add_transaction(username, f"Withdrew {amount} from balance.")
                messagebox.showinfo("Success", f"Withdrew {amount} from balance.")
            withdraw_window.destroy()

        tk.Button(withdraw_window, text="Withdraw", command=submit_withdraw, **button_style, width=10, height=2).pack(pady=10)

    def show_transactions():
        transactions_window = tk.Toplevel(dashboard)
        transactions_window.title("Transactions")
        transactions_window.configure(bg="lightblue")  
        tk.Label(transactions_window, text="Your Transactions:", bg="lightblue", font=("Georgia", 10, "bold")).pack()
        transactions = get_transactions(username)

        for transaction in transactions:
            tk.Label(transactions_window, text=transaction, bg="lightblue").pack()

    def transfer_money_gui() -> None:
        transfer_window = tk.Toplevel(dashboard)
        transfer_window.title("Transfer Money")
        transfer_window.configure(bg="lightblue") 

        tk.Label(transfer_window, text="Recipient Username:", bg="lightblue", font=("Georgia", 10, "bold")).pack()
        target_username_entry = tk.Entry(transfer_window)
        target_username_entry.pack()

        tk.Label(transfer_window, text="Amount:", bg="lightblue", font=("Georgia", 10, "bold")).pack()
        amount_entry = tk.Entry(transfer_window)
        amount_entry.pack()

        def submit_transfer() -> None:
            target_username = target_username_entry.get()
            amount = float(amount_entry.get())

            try:
                transfer_money(username, target_username, amount)
                messagebox.showinfo("Success", f"Transferred {amount} to {target_username}.")
                transfer_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(transfer_window, text="Transfer", command=submit_transfer, **button_style, width=10, height=2).pack(pady=10)

    tk.Button(dashboard, text="Show Balance", command=show_balance, **button_style, width=20, height=2).pack(pady=10)
    tk.Button(dashboard, text="Add Money", command=add_money, **button_style, width=20, height=2).pack(pady=10)
    tk.Button(dashboard, text="Withdraw Money", command=withdraw_money, **button_style, width=20, height=2).pack(pady=10)
    tk.Button(dashboard, text="Show Transactions", command=show_transactions, **button_style, width=20, height=2).pack(pady=10)
    tk.Button(dashboard, text="Transfer Money", command=transfer_money_gui, **button_style, width=20, height=2).pack(pady=10)
    tk.Button(dashboard, text="Log Out", command=dashboard.destroy, **button_style, width=20, height=2).pack(pady=10)





def start_gui() -> None:
    root = tk.Tk()
    root.title("Bank App")
    root.geometry("400x400")
    root.configure(bg="lightblue")

    tk.Label(root, text="OBank", font=("Georgia", 24, "bold",), fg="black", bg="lightblue").pack(pady=30)

    
    
    tk.Button(root, text="REGISTER", command=lambda: register_user_gui(root), **button_style).pack(pady=10, ipadx=30, ipady=8)
    tk.Button(root, text="LOGIN", command=lambda: login_user_gui(root), **button_style).pack(pady=10, ipadx=40, ipady=8)
    tk.Button(root, text="EXIT", command=root.destroy, **button_style).pack(pady=70, ipadx=10, ipady=10)

    root.mainloop()



if __name__ == "__main__":
    start_gui()
