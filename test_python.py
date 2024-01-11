import pymysql
import boto3
import os

import random
from datetime import datetime, timedelta

import mysql.connector

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
#print("Access key: "+ session.get_credentials().access_key)
#print("Secret key: " + session.get_credentials().secret_key)

#token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)    
#print("token: " + token)

#connection = pymysql.connect(host=ENDPOINT, user=USER, passwd=PASSWORD, port=PORT, database=DBNAME, connect_timeout=10, ssl_ca='global-bundle.pem')
#connection = mysql.connector.connect(host=ENDPOINT, user=USER, password=PASSWORD, port=PORT)
connection = pymysql.connect(host=ENDPOINT, user=USER, password=PASSWORD, port=PORT)
print("Connessione al database riuscita!")

try:
    if connection.is_connected():
        print(f"Connessione pymysql al database {DBNAME} riuscita.")
except mysql.connector.Error as e:
        print(f"Errore durante la connessione al database: {e}")
finally:
    if connection.is_connected():
        connection.close()
        print("Connessione al database chiusa.")