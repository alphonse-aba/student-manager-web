from django.urls import path
from . import views

urlpatterns = [
    path("", views.liste, name="liste"),
    path("ajouter/", views.ajouter, name="ajouter"),
    path("supprimer/<int:id>/", views.supprimer, name="supprimer"),
    path("ajouter_note/<int:id>/", views.ajouter_note, name="ajouter_note"),
    path("api/", views.api_etudiants, name="api_etudiants"),
    path("api/ajouter/", views.api_ajouter, name="api_ajouter"),  # ← ici !
    path("api/supprimer/<int:id>/", views.api_supprimer, name="api_supprimer"),
]