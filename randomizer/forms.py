from django import forms
from .models import *

class GameForm(forms.ModelForm):
    class Meta:
        model = Jeux
        fields = '__all__'

    """fields = Jeux._meta.get_fields()
    json_fields = [field.name for field in fields if isinstance(field, models.JSONField)]
    coop_choice = [
          (0, 'Non coopératif'),
          (1, 'Coopératif'),
          (2, 'En équipe'),
      ]"""


class randForm(forms.ModelForm):
    coop = forms.ChoiceField(required=False, choices = [
                                                     ("", ""),
                                                     (0, 'Compétitif'),
                                                     (1, 'Coopératif'),
                                                     (2, 'En équipe')
                                                 ])
    duree = forms.IntegerField(required=False)
    min_max = forms.ChoiceField(required=False, choices = [
                                                       ("minimum", 'minimum'),
                                                       ("maximum", 'maximum')
                                                   ])
    joueurs = forms.IntegerField(required=False)
    nb_result = forms.IntegerField(required=False)
    favori = forms.BooleanField(required=False)
    jamais_joué = forms.BooleanField(required=False)

    class Meta:
        model = Jeux
        fields = ["favori"]


class PartieForm(forms.ModelForm):
    #nom = forms.CharField(label="Nom du jeu", required=False, disabled=True)

    class Meta:
        model = Partie
        fields = ["duree", "nom"]
