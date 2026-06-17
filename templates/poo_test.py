# 1. On fabrique le moule (La Classe)
class Etudiant:
    # La fonction magique __init__ s'exécute AUTOMATIQUEMENT à la création de l'étudiant
    def __init__(self, prenom_recu):
        self.nom = prenom_recu  # Attribut : chaque étudiant aura son propre nom
        self.notes = []  # Attribut : chaque étudiant aura sa liste de notes


# --- UTILISATION DU MOULE ---

# 2. On crée deux vrais objets (des "instances") à partir du moule
etudiant1 = Etudiant("Alphonse")
etudiant2 = Etudiant("Lou")

# 3. On affiche les informations en utilisant le point "."
print(f"Le premier étudiant s'appelle : {etudiant1.nom}")
print(f"Le deuxième étudiant s'appelle : {etudiant2.nom}")