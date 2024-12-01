import random
import psycopg2
from psycopg2 import OperationalError
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
colors = {}
materials = {}
methods = {}

try:
    conn = psycopg2.connect(dbname="mrpo", user="postgres", password="1234", host="localhost")
    cursor = conn.cursor()

    data = pd.read_excel("data.xlsx")
    data = data.replace({np.nan: None})

    data['color'] = data['color'].fillna('-')
    data['material'] = data['material'].fillna('-')
    data['applicMetod'] = data['applicMetod'].fillna('-')

    cursor.execute('''SELECT * FROM "Colors"''')
    for row in cursor.fetchall():
        colors[row[1]] = row[0]
    cursor.execute('''SELECT * FROM "SouvenirMaterials"''')
    for row in cursor.fetchall():
        materials[row[1]] = row[0]
    cursor.execute('''SELECT * FROM "ApplicationMetods"''')
    for row in cursor.fetchall():
        methods[row[1]] = row[0]

    # Импорт в таблицу Souvenirs
    for index, row in data.iterrows():
        id = row['id']
        url = row['url']
        shortname = row['shortname']
        name = row['name']
        description = row['description']
        rating = row['rating']
        idCategory = row['categoryid']
        idColor = colors[row['color']]
        size = row['prodsize']
        idMaterial = materials[row['material']]
        weight = row['weight']
        qtypics = row['qtypics']
        picssize = row['picssize']
        idApplicMethod = methods[row['applicMetod']]
        allCategories = row['fullCategories']
        dealerprice = row['dealerPrice']
        price = row['price']
        commnets = row['currencyid']

        cursor.execute('''INSERT INTO "Souvenirs"
        ("ID", "URL", "ShortName", "Name", "Description",
        "Rating", "IdCategory", "IdColor", "Size",
        "IdMaterial", "Weight", "QTypics", "PicsSize",
        "IdApplicMethod", "AllCategories", "DealerPrice", "Price", "Comments")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (id, url, shortname, name, description,
                        rating, idCategory, idColor, size,
                        idMaterial, weight, qtypics, picssize,
                        idApplicMethod, allCategories, dealerprice, price, commnets))

    # Импорт в таблицу SouvenirStores
    cursor.execute('''SELECT "ID" FROM "Souvenirs"''')
    souvenirsId = []
    for row in cursor.fetchall():
        souvenirsId.append(row[0])

    cursor.execute('''SELECT "ID" FROM "SouvenirProcurements"''')
    procurementsId = []
    for row in cursor.fetchall():
        procurementsId.append(row[0])

    for _ in range(20):
        sId = random.choice(souvenirsId)
        pId = random.choice(procurementsId)

        amount = random.randint(1, 100000)
        commnets = fake.text(max_nb_chars=50)

        cursor.execute('''INSERT INTO "SouvenirStores" ("IdSouvenir", "IdProcurement", "Amount", "Comments")
        VALUES (%s, %s, %s, %s)''', (sId, pId, amount, commnets))

    # Импорт в таблицу ProcurementSouvenirs
    for _ in range(20):
        sId = random.choice(souvenirsId)
        pId = random.choice(procurementsId)
        amount = random.randint(1, 100000)
        price = random.random()

        cursor.execute('''INSERT INTO "ProcurementSouvenirs" ("IdSouvenir", "IdProcurement", "Amount", "Price")
        VALUES (%s, %s, %s, %s)''', (sId, pId, amount, price))
        pass

    conn.commit()
    cursor.close()
    conn.close()

except OperationalError as e:
    print(f"The error '{e}' occurred")