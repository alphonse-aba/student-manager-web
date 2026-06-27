from rest_framework import serializers
from .models import Etudiant, Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'valeur']

class EtudiantSerializer(serializers.ModelSerializer):
    notes = serializers.SerializerMethodField()

    class Meta:
        model = Etudiant
        fields = ['id', 'nom', 'notes']

    def get_notes(self, obj):
        notes = Note.objects.filter(etudiant=obj)
        return NoteSerializer(notes, many=True).data