
import time
import csv
from datetime import datetime


with open('weather_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), "Naam1", "Naam2", 
                         "Naam3", "Naam4", "Naam5",])

while True:
    
    Naam1 = "henk"
    Naam2 = "slim"
    Naam3 = "shrek"
    Naam4 = "alberto"
    Naam5 = "sendy" 
    
    tijdstip = datetime.now().strftime('%d-%m-%y %H:%M:%S')
    print(f"Tijdstip: {tijdstip}")
    print(Naam1)
    print(Naam2)
    print(Naam3)
    print(Naam4)
    print(Naam5)
    
    #schrijf naar excel
    with open('weather_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), Naam1, Naam2, 
                         Naam3, Naam4, Naam5,])
            
    time.sleep(3)