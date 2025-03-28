import sqlite3
import pandas as pd
import numpy as np
import os, sys
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