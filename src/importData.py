import psycopg2
from psycopg2 import OperationalError
import pandas as pd
import numpy as np

try:
    conn = psycopg2.connect(dbname="mrpo", user="postgres", password="1234", host="localhost")
    cursor = conn.cursor()

    data = pd.read_excel("data.xlsx")
    data = data.replace({np.nan: None})

    data['color'] = data['color'].astype("string")
    data['applicMetod'] = data['applicMetod'].astype("string")
    data['material'] = data['material'].astype("string")

    # Импорт в таблицу Colors
    colors = data['color'].unique()
    colors = colors.dropna()
    for color in colors:
        cursor.execute('''INSERT INTO "Colors" ("Name") VALUES (%s)''', (color,))
    cursor.execute('''INSERT INTO "Colors" ("Name") VALUES (%s)''', ('-',))

    # Импорт в таблицу ApplicationMetods
    methods = data['applicMetod'].unique()
    methods = methods.dropna()
    for method in methods:
        cursor.execute('''INSERT INTO "ApplicationMetods" ("Name") VALUES (%s)''', (method,))
    cursor.execute('''INSERT INTO "ApplicationMetods" ("Name") VALUES (%s)''', ('-',))

    # Импорт в таблицу SouvenirMaterials
    materials = data['material'].unique()
    materials = materials.dropna()
    for material in materials:
        cursor.execute('''INSERT INTO "SouvenirMaterials" ("Name") VALUES (%s)''', (material,))
    cursor.execute('''INSERT INTO "SouvenirMaterials" ("Name") VALUES (%s)''', ('-',))

    conn.commit()

    cursor.close()
    conn.close()

except OperationalError as e:
    print(f"The error '{e}' occurred")