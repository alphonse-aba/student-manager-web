import json
import os
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "cle_secrete_alphonse_2026"  # Nécessaire pour les sessions

FICHIER_DATA = "students.json"

# Identifiants de connexion (en dur pour l'instant)
ADMIN_USERNAME = "alphonse"
ADMIN_PASSWORD = "togo2026"


class Etudiant:
    def __init__(self, nom_recu):
        self.nom = nom_recu
        self.notes = []


def charger_les_etudiants():
    if not os.path.exists(FICHIER_DATA):
        return []
    with open(FICHIER_DATA, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def sauvegarder_les_etudiants(liste):
    with open(FICHIER_DATA, "w", encoding="utf-8") as f:
        json.dump(liste, f, indent=4, ensure_ascii=False)


# =========================================================
# 🔐 ROUTES LOGIN / LOGOUT (NOUVEAU)
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    erreur = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["connecte"] = True
            return redirect(url_for("page_accueill"))
        else:
            erreur = "Identifiants incorrects."
    return render_template("login.html", erreur=erreur)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# =========================================================
# TES ROUTES EXISTANTES (protégées par le login)
# =========================================================

@app.route("/", methods=["GET", "POST"])
def page_accueill():
    if not session.get("connecte"):
        return redirect(url_for("login"))

    liste_actuelle = charger_les_etudiants()

    if request.method == "POST":
        nom_saisi = request.form.get("prenom")
        if nom_saisi:
            existe = any(
                e["nom"].lower() == nom_saisi.lower() for e in liste_actuelle
            )
            if not existe:
                nouvel_objet = Etudiant(nom_saisi)
                donnees_etudiant = {
                    "nom": nouvel_objet.nom,
                    "notes": nouvel_objet.notes,
                }
                liste_actuelle.append(donnees_etudiant)
                sauvegarder_les_etudiants(liste_actuelle)

    return render_template("index.html", etudiants=liste_actuelle)


@app.route("/ajouter_note/<nom>", methods=["POST"])
def ajouter_note(nom):
    if not session.get("connecte"):
        return redirect(url_for("login"))

    liste_actuelle = charger_les_etudiants()
    note_saisie = request.form.get("note")

    if note_saisie:
        try:
            note_float = float(note_saisie)
            if 0 <= note_float <= 20:
                for etudiant in liste_actuelle:
                    if etudiant["nom"] == nom:
                        etudiant["notes"].append(note_float)
                        break
                sauvegarder_les_etudiants(liste_actuelle)
        except ValueError:
            pass

    return redirect("/")


@app.route("/supprimer/<nom>", methods=["POST"])
def supprimer_etudiant(nom):
    if not session.get("connecte"):
        return redirect(url_for("login"))

    liste_actuelle = charger_les_etudiants()
    liste_nettoyee = [e for e in liste_actuelle if e["nom"] != nom]
    sauvegarder_les_etudiants(liste_nettoyee)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
