import sqlite3
import os

# print("SQL")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_name = os.path.join(BASE_DIR, 'db.sqlite3')
# print(db_name)

# print(os.path.isfile(db_name))

def list_tables(db_path):
    """Returns a list of table names in the SQLite database at db_path."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    conn.close()

# print(list_tables(db_name))

def db_save(variable_name, value):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS data (variable TEXT PRIMARY KEY, value TEXT)")
    cursor.execute("INSERT INTO data (variable, value) VALUES (?, ?) ON CONFLICT(variable) DO UPDATE SET value = ?",
                   (variable_name, value, value))
    conn.commit()
    conn.close()


# "C:\Users\darre\PycharmProjects\hay_day\db.sqlite3"
# "C:\Users\darre\PycharmProjects\hay_day\db.sqlite3"
def db_load(variable_name):
    # print("DB Load:", db_name)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT value FROM data WHERE variable = ?", (variable_name,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except:
        return None

def db_delete_all():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM data")
    conn.commit()
    conn.close()

def db_print_all():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT variable, value FROM data")
    entries = cursor.fetchall()
    conn.close()

    print("DB Contents")
    if entries:
        for variable, value in entries:
            print(f" - {variable}: {value}")
    else:
        print("No entries found in the database.")


# print("SQL end")
