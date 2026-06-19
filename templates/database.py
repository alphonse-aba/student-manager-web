import sqlite3

def get_db():
    conn = sqlite3.connect("etudiants.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS etudiants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL
        )
    """)
    conn.execute("""
CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            etudiant_id INTEGER NOT NULL,
            valeur REAL NOT NULL,
            FOREIGN KEY (etudiant_id) REFERENCES etudiants(id)
        )
    """)
    conn.commit()
    conn.close()