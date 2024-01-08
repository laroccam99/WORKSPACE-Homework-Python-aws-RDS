import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Input da riga di comando
start_date = input("Insert start date (YYYY-MM-DD HH:MM:SS): ")
end_date = input("Insert end date (YYYY-MM-DD HH:MM:SS): ")

# Call API al server Flask (default http://localhost:5000), (/telemetry indicato nel server) ed estrazione dati
api_url = f"http://localhost:5000/telemetry?start_date={start_date}&end_date={end_date}"
response = requests.get(api_url)
telemetry_data = response.json()
times = [datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S') for data in telemetry_data]

# Generatore grafici: uno per ogni attributo
attributes = ['speed', 'rotation', 'power']
for attribute in attributes:
    values = [data[attribute] for data in telemetry_data]

    # Genera il grafico per l'attributo corrente
    plt.plot(times, values)
    plt.xlabel('Time')
    plt.ylabel(attribute.capitalize())
    plt.title(f'Telemetry Graph - {attribute.capitalize()}')
    plt.show()
