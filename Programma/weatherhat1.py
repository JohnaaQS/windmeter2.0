#!/usr/bin/env python3
 
import time
import csv
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from st7789 import ST7789
import weatherhat
 
print("""
Windmeter + LCD Display project
Made by JQS
""")
 
SPI_SPEED_MHZ = 80
 
# LCD aanmaken
disp = ST7789(
    rotation=90,
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    spi_speed_hz=SPI_SPEED_MHZ * 1000 * 1000,
)
 
#display starten
disp.begin()
WIDTH = disp.width
HEIGHT = disp.height
 
# Canvas aanmaken
img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
 
#import van het lettertype
font_path = "/home/rpi/weatherhat-python/.venv/lib/python3.11/site-packages/font_manrope/files/Manrope-Bold.ttf"
font_size = 20
font = ImageFont.truetype(font_path, font_size)
 
# Sensor initialiseren
sensor = weatherhat.WeatherHAT()
 
# CSV-bestand aanmaken
with open('weather_data.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Tijdstip", "Apparaat Temperatuur (°C)", "Temperatuur (°C)",
                     "Luchtdruk (hPa)", "Luchtvochtigheid (%)", "Lichtintensiteit (lux)",
                     "Windsnelheid (m/s)", "Windrichting (graden)"])
 
#waarde check aanmaken
def check_waarde(waarde):
    return "nvt" if waarde == 0 else round(waarde, 2)
 
try:
    while True:
        # Sensorwaarden ophalen
        tijdstip = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        apparaat_temperatuur = check_waarde(sensor.device_temperature)
        tempratuur = check_waarde(sensor.temperature)
        druk = check_waarde(sensor.pressure)
        vochtigheid = check_waarde(sensor.humidity)
        lux = check_waarde(sensor.lux)
        windkracht = check_waarde(sensor.wind_speed)
        windrichting = check_waarde(sensor.wind_direction)
 
        #Waarden printen in terminal
        print(f"Tijd: {tijdstip}")
        print(f"Apparaat Temp: {apparaat_temperatuur} °C")
        print(f"Temperatuur: {tempratuur} °C")
        print(f"Luchtdruk: {druk} hPa")
        print(f"Luchtvochtigheid: {vochtigheid} %")
        print(f"Lichtintensiteit: {lux} lux")
        print(f"Windsnelheid: {windkracht} m/s")
        print(f"Windrichting: {windrichting} graden")
        print("------------------------------------")
 
        # Op LCD-scherm tonen
        img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        message = f"Time: {tijdstip}\nWindrichting: {windrichting}°\nWindsnelheid: {windkracht} m/s\nTemp: {tempratuur}°C\nApparaat Temp: {apparaat_temperatuur}°C\nMade by JQS"
        draw.text((10, 10), message, font=font, fill=(255, 255, 255))
        disp.display(img)
 
        # Data opslaan in CSV
        with open('weather_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([tijdstip, apparaat_temperatuur, tempratuur,
                            druk, vochtigheid, lux, windkracht, windrichting])
            print("Gegevens opgeslagen!")
       
        # Git-push
        os.popen('/bin/auto_push.sh')
        print("git push succesvol!")
       
        sensor.update(interval=5)
        time.sleep(10)
#afsuiten van het programma
except KeyboardInterrupt:
    print("\nProgramma afgesloten. scherm schakelt uit..")
    disp.set_backlight(0)
 
 
 