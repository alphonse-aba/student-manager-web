from django.db import models

class Etudiant(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    valeur = models.FloatField()

    def __str__(self):
        return f"{self.etudiant.nom} - {self.valeur}"