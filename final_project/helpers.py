import sqlite3

DATABASE = "history.db"

def query_sql(query, *args):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(query, args)
    if query.split(" ")[0] == "SELECT":
        rows = cursor.fetchall()
        conn.close
        return rows
    else:
        conn.commit()
        conn.close()
