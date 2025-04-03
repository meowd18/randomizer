import sqlite3
import pandas as pd
import numpy as np
import os, sys
import datetime
from django.shortcuts import get_object_or_404
from randomizer.models import *
#from randomizer.models import Jeux

#"../jeux.ods", engine="odf"

def insert_data(ods_file):
    #insérer les données initiales
    from randomizer.models import Jeux
    df = pd.read_excel(ods_file)
    df = df.replace({np.nan: None})
    for index, row in df.iterrows():
        data = {col: row[col] for col in df.columns}
        Jeux.objects.create(**data)
    print('Great success !')

def insert_partie(jeu_id, duree):
    #modifier jamais joué
    jeu = get_object_or_404(Jeux, id=jeu_id)
    if jeu.jamais_joué == True:
        print("jamais joué")
        jeu.jamais_joué = False
        jeu.save()
    #enregistrer partie
    date = datetime.datetime.now()
    partie = Partie(date=date, duree=duree, nom_id=jeu_id)
    print(date, duree, jeu_id)
    partie.save()