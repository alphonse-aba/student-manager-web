import json
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

FICHIER_DATA = "students.json"


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


# --- ROUTE PRINCIPALE (Accueil & Ajout) ---
@app.route("/", methods=["GET", "POST"])
def page_accueill():
    liste_actuelle = charger_les_etudiants()

    if request.method == "POST":
        nom_saisi = request.form.get("prenom")

        if nom_saisi:
            # SÉCURITÉ ANTI-DOUBLON : On vérifie si le nom n'est pas déjà dans la liste
            if nom_saisi not in liste_actuelle:
                liste_actuelle.append(nom_saisi)
                sauvegarder_les_etudiants(liste_actuelle)

    return render_template("index.html", etudiants=liste_actuelle)


# --- NOUVELLE ROUTE : SUPPRIMER UN ÉTUDIANT ---
@app.route("/supprimer/<nom>", methods=["POST"])
def supprimer_etudiant(nom):
    liste_actuelle = charger_les_etudiants()

    # Si l'étudiant existe dans la liste, on le retire
    if nom in liste_actuelle:
        liste_actuelle.remove(nom)
        sauvegarder_les_etudiants(liste_actuelle)

    # Une fois supprimé, on recharge immédiatement la page d'accueil
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)