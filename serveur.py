import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "cle_secrete_alphonse_2026"

ADMIN_USERNAME = "alphonse"
ADMIN_PASSWORD = "togo2026"

# =========================================================
# BASE DE DONNÉES
# =========================================================

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

# =========================================================
# LOGIN / LOGOUT
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    erreur = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["connecte"] = True
            return redirect(url_for("page_accueil"))
        else:
            erreur = "Identifiants incorrects."
    return render_template("login.html", erreur=erreur)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# =========================================================
# ROUTES PRINCIPALES
# =========================================================

@app.route("/", methods=["GET", "POST"])
def page_accueil():
    if not session.get("connecte"):
        return redirect(url_for("login"))

    conn = get_db()

    if request.method == "POST":
        nom_saisi = request.form.get("prenom")
        if nom_saisi:
            existe = conn.execute(
                "SELECT * FROM etudiants WHERE LOWER(nom) = LOWER(?)",
                (nom_saisi,)
            ).fetchone()
            if not existe:
                conn.execute(
                    "INSERT INTO etudiants (nom) VALUES (?)",
                    (nom_saisi,)
                )
                conn.commit()

    # Récupérer tous les étudiants avec leurs notes
    etudiants = conn.execute("SELECT * FROM etudiants").fetchall()
    
    liste = []
    for e in etudiants:
        notes = conn.execute(
            "SELECT valeur FROM notes WHERE etudiant_id = ?",
            (e["id"],)
        ).fetchall()
        valeurs = [n["valeur"] for n in notes]
        liste.append({
            "id": e["id"],
            "nom": e["nom"],
            "notes": valeurs
        })

    conn.close()
    return render_template("index.html", etudiants=liste)


@app.route("/ajouter_note/<int:id>", methods=["POST"])
def ajouter_note(id):
    if not session.get("connecte"):
        return redirect(url_for("login"))

    note_saisie = request.form.get("note")
    if note_saisie:
        try:
            note_float = float(note_saisie)
            if 0 <= note_float <= 20:
                conn = get_db()
                conn.execute(
                    "INSERT INTO notes (etudiant_id, valeur) VALUES (?, ?)",
                    (id, note_float)
                )
                conn.commit()
                conn.close()
        except ValueError:
            pass

    return redirect("/")


@app.route("/supprimer/<int:id>", methods=["POST"])
def supprimer_etudiant(id):
    if not session.get("connecte"):
        return redirect(url_for("login"))

    conn = get_db()
    conn.execute("DELETE FROM notes WHERE etudiant_id = ?", (id,))
    conn.execute("DELETE FROM etudiants WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)