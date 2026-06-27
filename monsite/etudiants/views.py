from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import Etudiant, Note
from .serializers import EtudiantSerializer
import json

# Vue HTML classique
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

# Anciennes API
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

# Nouvelles API avec DRF
@api_view(['GET'])
def drf_liste(request):
    etudiants = Etudiant.objects.all()
    serializer = EtudiantSerializer(etudiants, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def drf_ajouter(request):
    if not request.user.is_authenticated:
        return Response({"error": "Non autorisé !"}, status=401)
    serializer = EtudiantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
def drf_supprimer(request, id):
    if not request.user.is_authenticated:
        return Response({"error": "Non autorisé !"}, status=401)
    etudiant = Etudiant.objects.get(id=id)
    etudiant.delete()
    return Response({"success": True})