# On importe l'outil pour créer des URLs
from django.urls import path

# On importe toutes nos fonctions depuis views.py
from . import views  # le point "." signifie "dans ce même dossier"

# Liste des URLs de l'app etudiants
urlpatterns = [
    # http://127.0.0.1:8000/etudiants/ → affiche la liste des étudiants
    path("", views.liste, name="liste"),

    # http://127.0.0.1:8000/etudiants/ajouter/ → ajoute un étudiant
    path("ajouter/", views.ajouter, name="ajouter"),

    # http://127.0.0.1:8000/etudiants/supprimer/1/ → supprime l'étudiant avec id=1
    path("supprimer/<int:id>/", views.supprimer, name="supprimer"),

    # http://127.0.0.1:8000/etudiants/ajouter_note/1/ → ajoute une note à l'étudiant id=1
    path("ajouter_note/<int:id>/", views.ajouter_note, name="ajouter_note"),
]