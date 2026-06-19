from django.shortcuts import render, redirect
from .models import Etudiant, Note

def liste(request):
    etudiants = Etudiant.objects.all()
    return render(request, "etudiants/liste.html", {"etudiants": etudiants})

def ajouter(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        if nom:
            Etudiant.objects.create(nom=nom)
    return redirect("liste")

def supprimer(request, id):
    etudiant = Etudiant.objects.get(id=id)
    etudiant.delete()
    return redirect("liste")

def ajouter_note(request, id):
    if request.method == "POST":
        valeur = request.POST.get("valeur")
        if valeur:
            etudiant = Etudiant.objects.get(id=id)
            Note.objects.create(etudiant=etudiant, valeur=float(valeur))
    return redirect("liste")