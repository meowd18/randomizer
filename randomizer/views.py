from django.shortcuts import render, redirect
from .models import Jeux
from .forms import *
from django.db.models import Q
import random

# Create your views here.
def accueil(request):
    #page d'accueil
    #initialisation
    form_random = randForm()
    msg = ""
    x = ""
    liste_jeux = []

    #si envoi de formulaire
    if request.method == 'POST':
        if 'find' in request.POST:
            form_random = randForm(request.POST)
            if not form_random.is_valid():
                msg = str(form_pat.errors)
                print(msg)

            else:
                #récupération des données du formulaire
                duree = form_random.cleaned_data['duree']
                joueurs = form_random.cleaned_data['joueurs']
                coop = form_random.cleaned_data['coop']
                min_max = form_random.cleaned_data['min_max']
                nb_result = form_random.cleaned_data['nb_result']
                favori = form_random.cleaned_data['favori']
                jamais_joué = form_random.cleaned_data['jamais_joué']

                if coop == "0":
                    x = "compétitif"
                elif coop == "1":
                    x = "en coop"
                elif coop == "2":
                    x = "en équipe"
                elif coop == "":
                    x = None

#                random = Jeux.objects.order_by('?').first()

                #trouver jeux selon critères
                #print(f"ok je cherche un jeu pour {joueurs} joueur{'s' if joueurs > 1 else ''} qui dure {min_max} {duree} minutes {'et qui soit ' + x if x else ''}")

                filters = Q()

                if x:
                    filters &= Q(coop=coop)

                if duree is not None:
                    if min_max == "minimum":
                        filters &= Q(duree_max__gte=duree)
                    elif min_max == "maximum":
                        filters &= Q(duree_min__lte=duree)

                if joueurs is not None:
                    filters &= Q(joueurs_min__lte=joueurs) & Q(joueurs_max__gte=joueurs)

                if favori:
                    filters &= Q(favori=True)
                if jamais_joué:
                    filters &= Q(jamais_joué=True)

                if filters == Q():
                    results = Jeux.objects.order_by('?').first()
                    liste_jeux.append(results.nom)
                else:
                    results = Jeux.objects.filter(filters)

                    #print(f"J'ai trouvé {len(results)} résultat{"s" if len(results) > 1 else ""}")

                    for jeu in results:
                        #print(jeu.nom)
                        liste_jeux.append(jeu.nom)

                if nb_result:
                    liste_jeux = random.sample(liste_jeux, nb_result)

                if len(liste_jeux) == 0:
                    msg = "Aucun jeu ne correspond à ces critères"

    return render(request, "accueil.html",
                            {'form_random': form_random,
                                    'msg': msg,
                                    'liste_jeux': liste_jeux})

def index(request):
    return redirect("accueil")

def insert(request):
    #insérer nouveaux jeux dans la BDD
        form_game = GameForm()
        msg = ""
        if request.method == 'POST':
            if 'insert' in request.POST:
                form_game = GameForm(request.POST)
                if not form_game.is_valid():
                    msg = str(form_pat.errors)
                    print(msg)
                else:
                    try:
                        new_game = form_game.save()
                        print(new_game)
                        if new_game:
                            msg = "Jeu ajouté avec succès."
                    except Exception as e:
                        msg = str(e)
                        print(f"Informations sur l'erreur: {msg}")


        return render(request, "insert.html",
        {'form_game': form_game,
        'msg': msg})
