import weatherhat
import time
import csv
from datetime import datetime

sensor = weatherhat.WeatherHAT()

with open('weather_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Tijdstip", "Apparaat Temperatuur (°C)", "Temperatuur (°C)",
                     "Luchtdruk (hPa)", "Luchtvochtigheid (%)", "Lichtintensiteit (lux)", 
                     "Windsnelheid (m/s)", "Windrichting (graden)"])

while True:
 apparaat_tempratuur = sensor.device_temprature
 tempratuur = sensor.temprature
 druk = sensor.pressure
 vochtigheid = sensor.humidity
 lux = sensor.lux
 windkracht = sensor.wind
 windrichting = sensor.wind_direction
 
 print(f"Apparaat temperatuur: {apparaat_tempratuur:.2f} °C")
 print(f"tempratuur: {tempratuur:.2f}")
 print(f"luchtdruk: {druk:.2f} hPa")
 print(f"Luchtvochtigheid: {vochtigheid:.2f} %")
 print(f"Lichtintensiteit: {lux:.2f} lux")
 print(f"Windsnelheid: {windkracht:.2f} m/s")
 print(f"Windrichting: {windrichting:.2f} graden")
 
 with open('weather_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), apparaat_temperatuur, temperatuur, 
                         druk, vochtigheid, lux, windkracht, windrichting])
 
 sensor.update(interval=5)
 time.sleep(1)
 
