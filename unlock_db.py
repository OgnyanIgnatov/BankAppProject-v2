import sqlite3

#open db
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# unlock db
cursor.execute("PRAGMA locking_mode=EXCLUSIVE;")
cursor.execute("PRAGMA journal_mode=DELETE;")
conn.commit()

# close
cursor.close()
conn.close()
