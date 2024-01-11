import mysql.connector
import os

import random
from datetime import datetime, timedelta

ENDPOINT="database-1.cjug0u60whdi.eu-central-1.rds.amazonaws.com"
PORT=3306
USER="admin"
PASSWORD="password"
REGION="eu-central-1"
DBNAME="database_1_name"
SSLCERTIFICATE = 'global-bundle.pem'

os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#gets the credentials from .aws/credentials
#session = boto3.Session(profile_name='default')
#client = session.client('rds')
#token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)    
#print("token: " + token)

connection = mysql.connector.connect(host=ENDPOINT, user=USER, password=PASSWORD, port=PORT, db=DBNAME)
try:
    if connection.is_connected():
        print(f"Connessione al database {DBNAME} riuscita.")

        create_table_query = """
        CREATE TABLE IF NOT EXISTS RobotTelemetry (
            id INT AUTO_INCREMENT PRIMARY KEY,
            speed DECIMAL(10, 2),
            rotation DECIMAL(10, 2),
            time DATETIME,
            power INT
        )
        """
        with connection.cursor() as cursor:     #crea il cursore per scorrere risultati ed eseguire query
            print(f"Cursore creato correttamente")
            cursor.execute(create_table_query)  #esegue la query
            print(f"Query eseguita correttamente")
        connection.commit()                     #conferma creazione della tabella

        insert_query = """
        INSERT INTO RobotTelemetry (speed, rotation, time, power)
        VALUES (%s, %s, %s, %s)
        """

        def generate_random_tuple():
            speed = round(random.uniform(1.0, 3.0), 2)
            rotation = round(random.uniform(10.0, 90.0), 2)
            date_time = datetime.now() - timedelta(days=random.randint(1, 365), hours=random.randint(1, 24))
            date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
            power = random.randint(50, 200)
            return (speed, rotation, date_time_str, power)

        def generate_random_tuples(num_tuples, records_to_insert):
            for _ in range(num_tuples - len(records_to_insert)):
                records_to_insert.append(generate_random_tuple())

            return records_to_insert

        num_tuples_to_generate = 1000  #Numero desiderato di tuple
        records_to_insert = []
        generated_tuples = generate_random_tuples(num_tuples_to_generate, records_to_insert)
        print(f"{num_tuples_to_generate} Tuple generate correttamente")
        for record in generated_tuples:
            print(record)

        with connection.cursor() as cursor:
            cursor.executemany(insert_query, records_to_insert)
            print(f"Query eseguita correttamente")
        connection.commit()

except mysql.connector.Error as e:
    print(f"Errore durante la connessione al database: {str(e)}")

finally:
    try:
        if connection.is_connected():
            connection.close()
            print("Connessione al database chiusa.")
    except Exception as e:
        print(f"Errore durante la chiusura della connessione al database: {str(e)}")
