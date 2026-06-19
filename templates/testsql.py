import sqlite3
# 1. connexion (crée le fichier si il n'existe pas )
conn =sqlite3.connect("ecole.db")
#2.  crée la table etudiants
conn.execute("""
    CREATE TABLE IF NOT EXISTS etudiants(
            id integer primary key AUTOINCREMENT,
            nom TEXT NOT NULL
            )
            """)
#3. insérer des étudiants
conn.execute("INSERT INTO etudiants(nom) VALUES (?)",("Alphonse",))
conn.execute("INSERT INTO etudiants(nom) VALUES (?)",("Alou",))
conn. commit()
# 4. LIre tous les étudiants
etudiants=conn.execute("SELECT * FROM etudiants").fetchall()
for e in etudiants:
    print(f"ID:{e[0]} | Nom: {e[1]}")

                # 5. Modifier un étudiant
conn.execute("UPDATE etudiants SET nom = ? WHERE id = ?", ("Alphonse Abafoum", 1))
conn.commit()

# Vérifier le changement
etudiants = conn.execute("SELECT * FROM etudiants").fetchall()
print("\nAprès modification :")
for e in etudiants:
    print(f"ID:{e[0]} | Nom: {e[1]}") 
    # 6. Supprimer un étudiant
conn.execute("DELETE FROM etudiants WHERE id = ?", (2,))
conn.commit()

# Vérifier la suppression
etudiants = conn.execute("SELECT * FROM etudiants").fetchall()
print("\nAprès suppression :")
for e in etudiants:
    print(f"ID:{e[0]} | Nom: {e[1]}") 
    conn.close()                 
