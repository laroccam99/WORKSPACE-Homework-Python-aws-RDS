import random
from datetime import datetime, timedelta
count = 0
def generate_random_tuple(count):
            #count = count+1
            speed = round(random.uniform(1.0, 3.0), 2)
            rotation = round(random.uniform(10.0, 90.0), 2)
            date_time = datetime.now() - timedelta(days=random.randint(1, 365), hours=random.randint(1, 24))
            date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
            power = random.randint(50, 200)
            return (count, speed, rotation, date_time_str, power)

def generate_random_tuples(num_tuples, records_to_insert, count):
    for _ in range(num_tuples - len(records_to_insert)):
        records_to_insert.append(generate_random_tuple(count))
        count=count+1

    return records_to_insert

num_tuples_to_generate = 50  #Numero desiderato di tuple
records_to_insert = []
generated_tuples = generate_random_tuples(num_tuples_to_generate, records_to_insert, count)

for record in generated_tuples:
    print(record)