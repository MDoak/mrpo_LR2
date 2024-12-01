import random
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import OperationalError
from faker import Faker

fake = Faker()
statuses = ["pending_queued", "pending_error", "pending",
            "partly_reserved", "confirmed", "assembling",
            "assembled", "delivery", "processing", "complete",
            "cancel", "return", "partly_return"]
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 1, 1)

try:
    conn = psycopg2.connect(dbname="mrpo", user="postgres", password="1234", host="localhost")
    cursor = conn.cursor()

    # Импорт в таблицу Providers
    for _ in range(20):
        name = fake.company()
        email = fake.company_email()
        contact_person = fake.name()
        comments = fake.text(max_nb_chars=50)

        cursor.execute('''INSERT INTO "Providers" ("Name", "Email", "ContactPerson", "Comments")
        VALUES (%s, %s, %s, %s)''', (name, email, contact_person, comments))

    # Импорт в таблицу ProcurementStatuses
    for status in statuses:
        cursor.execute('''INSERT INTO "ProcurementStatuses" ("Name") VALUES (%s)''', (status,))

    # Импорт в табицу SouvenirProcurements
    cursor.execute('''SELECT "ID" FROM "Providers"''')
    providersId = []
    for row in cursor.fetchall():
        providersId.append(row[0])

    cursor.execute('''SELECT "ID" FROM "ProcurementStatuses"''')
    statusesId = []
    for row in cursor.fetchall():
        statusesId.append(row[0])

    for _ in range(50):
        pId = random.choice(providersId)
        sId = random.choice(statusesId)
        random_date = fake.date_time_between(start_date=start_date, end_date=end_date)
        converted_date = datetime.strftime(random_date, "%d-%m-%Y")
        cursor.execute('''INSERT INTO "SouvenirProcurements" ("IdProvider", "Date", "IdStatus")
        VALUES (%s, %s, %s)''', (pId, random_date, sId))

    conn.commit()
    cursor.close()
    conn.close()
except OperationalError as e:
    print(f"The error '{e}' occurred")