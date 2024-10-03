"""
#download op raspberry 
sudo apt update
sudo apt install python3-pip
pip3 install pimoroni-bme280 smbus

"""



import time
from smbus2 import SMBus
from bme280 import BME280
import csv
from datetime import datetime

# Initialiseer de I2C-bus en de BME280-sensor
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# Functie om data op te halen van de sensoren
def read_weather_data():
    tempratuur = bme280.get_temperature()
    druk = bme280.get_pressure()
    vochtigheid = bme280.get_humidity()

    # Print de gegevens
    print(f"Temperatuur: {tempratuur:.2f} °C")
    print(f"Luchtdruk: {druk:.2f} hPa")
    print(f"Luchtvochtigheid: {vochtigheid:.2f} %")

    return {
        "tempratuur": tempratuur,
        "druk": druk,
        "vochtigheid": vochtigheid
    }
    
def save_data_to_csv(data):
    with open('weather_data.csv', mode='a') as file:
        writer = csv.writer(file)
        # Voeg een regel met de timestamp en data toe aan het CSV-bestand
        writer.writerow([datetime.now(), data['tempratuur'], data['druk'], data['vochtigheid']])


# Herhaal de metingen elke 5 seconden (voorbeeld)
while True:
    data = read_weather_data()
    save_data_to_csv(data)
    time.sleep(5)
