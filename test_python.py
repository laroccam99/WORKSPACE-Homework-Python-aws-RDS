import mysql.connector
import os
from datetime import datetime, timedelta

ENDPOINT='tutorial-database-1.cjug0u60whdi.eu-central-1.rds.amazonaws.com'
PORT=3306
USER='admin'
PASSWORD='password'
REGION='eu-central-1'
DBNAME='tutorial-database-1'
#SSLCERTIFICATE = 'global-bundle.pem'

os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#gets the credentials from .aws/credentials
#session = boto3.Session(profile_name='default')
#client = session.client('rds')
#token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)    
#print("token: " + token)

#connection = pymysql.connect(host=ENDPOINT, user=USER, passwd=PASSWORD, port=PORT, database=DBNAME, connect_timeout=10, ssl_ca='global-bundle.pem')
connection = mysql.connector.connect(host=ENDPOINT, user=USER, password=PASSWORD, port=PORT, db=DBNAME)
create_table_query = """
        CREATE TABLE IF NOT EXISTS RobotTelemetry (
            id INT AUTO_INCREMENT PRIMARY KEY,
            speed DECIMAL(10, 2),
            rotation DECIMAL(10, 2),
            time DATETIME,
            power INT
        )"""
insert_query = """
        INSERT INTO RobotTelemetry (speed, rotation, time, power)
        VALUES (%s, %s, %s, %s)"""

try:
    if connection.is_connected():
        print(f"Connessione al database {DBNAME} riuscita.")
        cur = connection.cursor()
        print(f"Cursore creato correttamente")
        cur.execute(create_table_query)
        connection.commit() 
except mysql.connector.Error as e:
        print(f"Errore durante la connessione al database: {e}")
finally:
    try:
        if connection.is_connected():
            connection.close()
            print("Connessione al database chiusa.")
    except Exception as e:
        print(f"Errore durante la chiusura della connessione al database: {str(e)}")