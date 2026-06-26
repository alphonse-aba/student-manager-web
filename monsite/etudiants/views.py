from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Etudiant, Note
import json

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

def api_etudiants(request):
    etudiants = Etudiant.objects.all()
    data = []
    for etudiant in etudiants:
        data.append({
            "id": etudiant.id,
            "nom": etudiant.nom,
        })
    return JsonResponse({"etudiants": data})

@csrf_exempt
def api_ajouter(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nom = data.get("nom")
        if nom:
            etudiant = Etudiant.objects.create(nom=nom)
            return JsonResponse({"success": True, "id": etudiant.id, "nom": etudiant.nom})
    return JsonResponse({"success": False})
@csrf_exempt
def api_supprimer(request, id):
    if request.method == "DELETE":
        etudiant = Etudiant.objects.get(id=id)
        etudiant.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})