import time
import os
import csv
from datetime import datetime
import RPi.GPIO as GPIO
from smbus2 import SMBus
from bme280 import BME280
import spidev

# Instellingen voor het opslaan van gegevens
OUTPUT_FILE = 'weerdata.csv'
X_AANTAL_METINGEN = 10  # Sla gegevens op na X metingen

# GPIO-pin configuratie (voorbeeld)
WINDSNELHEID_PIN = 17  # Vervang door de juiste pin
WINDRICHTING_PIN = 18  # Vervang door de juiste pin
REGENVAL_PIN = 27      # Vervang door de juiste pin

# Functie om data van de Weather HAT te lezen
def read_windsnelheid():
    # Hier de code om windsnelheid van de sensor uit te lezen
    return 5.6  # Voorbeeldwaarde, vervang met sensor data

def read_windrichting():
    # Hier de code om windrichting van de sensor uit te lezen
    return 270  # Voorbeeldwaarde, vervang met sensor data

def read_regenval():
    # Hier de code om regenval van de sensor uit te lezen
    return 1.2  # Voorbeeldwaarde, vervang met sensor data

# Functie om gegevens naar CSV te schrijven
def schrijf_naar_csv(gegevens):
    bestand_bestaat = os.path.isfile(OUTPUT_FILE)
    with open(OUTPUT_FILE, 'a', newline='') as csvfile:
        veldnamen = ['Tijdstip', 'Windsnelheid', 'Windrichting', 'Regenval', 'metingen']
        writer = csv.DictWriter(csvfile, fieldnames=veldnamen)
        
        if not bestand_bestaat:
            writer.writeheader()
        
        writer.writerow(gegevens)

# Hoofdprogramma
def main():
    metingen_teller = 0
    while True:
        tijdstip = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        windsnelheid = read_windsnelheid()
        windrichting = read_windrichting()
        regenval = read_regenval()

        gegevens = {
            'Tijdstip': tijdstip,
            'Windsnelheid': windsnelheid,
            'Windrichting': windrichting,
            'Regenval': regenval,
            'metingen' : metingen_teller
            
            
        }
        
        print(f"Gegevens verzameld: {gegevens}")
        
        metingen_teller += 1

        if metingen_teller >= X_AANTAL_METINGEN:
            schrijf_naar_csv(gegevens)
            print(f"Gegevens opgeslagen in {OUTPUT_FILE}")
            metingen_teller = 0
        
        # Wacht 1 minuut (60 seconden) tussen metingen
        time.sleep(60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Programma gestopt.")
        GPIO.cleanup()





