import pymysql
import boto3
import os

import random
from datetime import datetime, timedelta

ENDPOINT="tutorial-database-1.cjug0u60whdi.eu-central-1.rds.amazonaws.com"
PORT=3306
USER="admin"
REGION="eu-central-1"
DBNAME="tutorial-database-1"
SSLCERTIFICATE = 'global-bundle.pem'

os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')
#print("Access key: "+ session.get_credentials().access_key)
#print("Secret key: " + session.get_credentials().secret_key)

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)    
#print("token: " + token)

connection = pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, connect_timeout=10, ssl_ca='global-bundle.pem')
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
            cursor.execute(create_table_query)  #esegue la query
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

        for record in generated_tuples:
            print(record)

        with connection.cursor() as cursor:
            cursor.executemany(insert_query, records_to_insert)
        connection.commit()

except Exception as e:
    print(f"Errore durante la connessione al database: {str(e)}")

finally:
    if connection.is_connected():
        connection.close()
        print("Connessione al database chiusa.")
