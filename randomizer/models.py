from django.db import models

# Create your models here.
class Jeux(models.Model):
    '''
    nom du jeu
    nombre de joueurs min
    nombre de joueurs max
    durée min
    durée max
    compétitif/coop/équipe

    COOP_CHOICES = [
        (0, 'Non coopératif'),
        (1, 'Coopératif'),
        (2, 'En équipe'),
    ]
    '''
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=250, db_index=True, unique=True)
    joueurs_min = models.IntegerField()
    joueurs_max = models.IntegerField()
    duree_min = models.IntegerField()
    duree_max = models.IntegerField()
    favori = models.BooleanField(null=True)
    jamais_joué = models.BooleanField(null=True)
    coop = models.BooleanField(null=True)
    competitif = models.BooleanField(null=True)
    equipe = models.BooleanField(null=True)

class Partie(models.Model):
    '''
    date
    jeu
    durée de la partie
    '''
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    duree = models.IntegerField()
    nom = models.ForeignKey(Jeux, on_delete=models.CASCADE)