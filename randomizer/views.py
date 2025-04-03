from django.shortcuts import render, redirect, get_object_or_404
from .models import Jeux
from .forms import *
from djangomizer.utils import *
from django.db.models import Q
import random
from django.http import JsonResponse
import datetime
from django.db.models import Avg



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
                msg = str(form_random.errors)
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

                filters = Q()

                if coop == "0":
                    x = "competitif"
                    filters &= Q(competitif=True)
                elif coop == "1":
                    x = "coop"
                    filters &= Q(coop=True)
                elif coop == "2":
                    x = "equipe"
                    filters &= Q(equipe=True)
                elif coop == "":
                    x = None

                #random = Jeux.objects.order_by('?').first()

                #trouver jeux selon critères
                #print(f"ok je cherche un jeu pour {joueurs} joueur{'s' if joueurs > 1 else ''} qui dure {min_max} {duree} minutes {'et qui soit ' + x if x else ''}")



                '''if x:
                    filters &= Q(coop=coop)

                if duree is not None:
                    if min_max == "minimum":
                        filters &= Q(duree_max__gte=duree)
                    elif min_max == "maximum":
                        filters &= Q(duree_min__lte=duree)'''

                if joueurs is not None:
                    filters &= Q(joueurs_min__lte=joueurs) & Q(joueurs_max__gte=joueurs)

                if favori:
                    filters &= Q(favori=True)
                if jamais_joué:
                    filters &= Q(jamais_joué=True)

                if filters == Q():
                    results = Jeux.objects.order_by('?').first()
                    liste_jeux.append(results)
                else:
                    results = Jeux.objects.filter(filters)

                    #print(f"J'ai trouvé {len(results)} résultat{"s" if len(results) > 1 else ""}")

                    for jeu in results:
                        #print(jeu.nom)
                        liste_jeux.append(jeu)

                if nb_result and nb_result <= len(liste_jeux):
                    liste_jeux = random.sample(liste_jeux, nb_result)

                if len(liste_jeux) == 0:
                    msg = "Aucun jeu ne correspond à ces critères"
                    return render(request, "accueil.html",
                                            {'form_random': form_random,
                                                    'msg': msg})


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
                    msg = str(form_game.errors)
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

def parties(request):
    partie_form = PartieForm()
    msg = ""
    if request.method == "POST":
        partie_form = PartieForm(request.POST)
        if not partie_form.is_valid():
            msg = str(partie_form.errors)
            print("ERREUR: ", msg)
        else:
            duree = partie_form.cleaned_data['duree']
            jeu = partie_form.cleaned_data['nom']
            jeu_id = jeu.id
            try:
                insert_partie(jeu_id, duree)
                msg = "Partie enregistrée"
                return render(request, "parties.html",
                    {'partie_form': partie_form,
                    'msg': msg})
            except Exception as e:
                msg = str(e)
                print(f"Informations sur l'erreur: {msg}")

        #get jeu_id from form
    return render(request, "parties.html",
        {'partie_form': partie_form,
        'msg': msg})


def get_form(request):
    if request.method == "GET":
        jeu_id = request.GET.get("jeu_id")
        game = get_object_or_404(Jeux, id=jeu_id)
        jeu = game.nom
        return render(request, "partie_popup.html",
        {'partie_form': partie_form,
        "jeu": game})

    if request.method == "POST":
        jeu_nom = request.POST.get("jeu")
        jeu_id = request.POST.get("jeu_id")
        duree = request.POST.get("duree")
        if not duree:
            msg = str(partie_form.errors)
            print("ERREUR: ", msg)
        else:
            try:
                duree = request.POST.get("duree")
                insert_partie(jeu_id, duree)

            except Exception as e:
                msg = str(e)
                print(f"Informations sur l'erreur: {msg}")


        return JsonResponse({"message": "Partie enregistrée avec succès !"})

def update(request):
    jeux = Jeux.objects.all()
    need_update = []
    dict = {}
    for jeu in jeux:
        moy = Partie.objects.filter(nom=jeu.id).aggregate(moyenne_duree=Avg('duree'))
        moyenne = moy["moyenne_duree"]
        if moyenne:
            duree_min = jeu.duree_min
            duree_max = jeu.duree_max
            if moyenne > duree_max:
                dict= {"jeu" : jeu.nom,
                "moyenne" : moyenne,
                "duree_max" : duree_max}
                need_update.append(dict)
            elif moyenne < duree_min:
                dict= {"jeu" : jeu.nom,
                "moyenne" : moyenne,
                "duree_min" : duree_min}
                need_update.append(dict)
    if len(need_update) == 0:
        return redirect("accueil")
    else:
        return render(request, "update.html",
                    {'need_update': need_update})

