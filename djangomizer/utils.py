import sqlite3
import pandas as pd
import os, sys
#from randomizer.models import Jeux

'''def insert_data():
    #insérer les données initiales
    from randomizer.models import Jeux
    df = pd.read_excel("../jeux.ods", engine="odf")
    for index, row in df.iterrows():
        data = {col: row[col] for col in df.columns}
        Jeux.objects.create(**data)
    print('Great success !')'''