import sqlite3

def db_save(variable_name, value, db_name="saved_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS data (variable TEXT PRIMARY KEY, value TEXT)")
    cursor.execute("INSERT INTO data (variable, value) VALUES (?, ?) ON CONFLICT(variable) DO UPDATE SET value = ?",
                   (variable_name, value, value))
    conn.commit()
    conn.close()


def db_load(variable_name, db_name="saved_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM data WHERE variable = ?", (variable_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def db_all(db_name="saved_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT variable, value FROM data")
    entries = cursor.fetchall()
    conn.close()

    if entries:
        for variable, value in entries:
            print(f"{variable}: {value}")
    else:
        print("No entries found in the database.")


# db_all()