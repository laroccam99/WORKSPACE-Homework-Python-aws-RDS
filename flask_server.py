from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/telemetry', methods=['GET'])
def get_telemetry_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Connessione al database
    db_config = {
        'user': 'admin',
        'password': 'password',
        'host': 'tutorial-database-1.cjug0u60whdi.eu-central-1.rds.amazonaws.com',
        'database': 'tutorial-database-1',
        'raise_on_warnings': True
    }
    connection = mysql.connector.connect(**db_config)

    query = f"""SELECT speed, rotation, time, power
    FROM RobotTelemetry
    WHERE time BETWEEN '{start_date}' AND '{end_date}'"""

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    connection.close()

    # Formattazione dati come una lista di dizionari
    telemetry_data = [
        {'speed': str(row[0]), 'rotation': row[1], 'time': row[2], 'power': row[3]}
        for row in result
    ]
    return jsonify(telemetry_data)

if __name__ == '__main__':
    app.run(debug=True)
