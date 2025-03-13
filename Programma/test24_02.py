import weatherhat

import time

import csv

from datetime import datetime

import os

import subprocess

from inky.auto import auto

from PIL import Image, ImageDraw, ImageFont
 
# Initialiseer sensor en scherm

sensor = weatherhat.WeatherHAT()

inky = auto()

inky.set_border(inky.WHITE)
 
# Font instellen voor tekstweergave

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
 
with open('weather_data.csv', mode='w', newline='') as file:

    writer = csv.writer(file)

    writer.writerow(["Tijdstip", "Apparaat Temperatuur (°C)", "Temperatuur (°C)",

                     "Luchtdruk (hPa)", "Luchtvochtigheid (%)", "Lichtintensiteit (lux)",

                     "Windsnelheid (m/s)", "Windrichting (graden)"])
 
while True:

    # Sensorwaarden uitlezen

    apparaat_temperatuur = sensor.device_temperature

    tempratuur = sensor.temperature

    druk = sensor.pressure

    vochtigheid = sensor.humidity

    lux = sensor.lux

    windkracht = sensor.wind_speed

    windrichting = sensor.wind_direction

    # Console output

    print(f"Apparaat temperatuur: {apparaat_temperatuur:.2f} °C")

    print(f"Temperatuur: {tempratuur:.2f} °C")

    print(f"Luchtdruk: {druk:.2f} hPa")

    print(f"Luchtvochtigheid: {vochtigheid:.2f} %")

    print(f"Lichtintensiteit: {lux:.2f} lux")

    print(f"Windsnelheid: {windkracht:.2f} m/s")

    print(f"Windrichting: {windrichting:.2f} graden")

    # Waarden opslaan in CSV

    with open('weather_data.csv', mode='a', newline='') as file:

        writer = csv.writer(file)

        writer.writerow([datetime.now(), apparaat_temperatuur, tempratuur,

                         druk, vochtigheid, lux, windkracht, windrichting])
 
    # ---- Inky Scherm Update ----

    img = Image.new("P", (inky.width, inky.height), inky.WHITE)

    draw = ImageDraw.Draw(img)

    text = (

        f"T: {tempratuur:.1f}°C  Druk: {druk:.0f}hPa\n"

        f"Vocht: {vochtigheid:.0f}%  Licht: {lux:.0f}lx\n"

        f"Wind: {windkracht:.1f}m/s  Richting: {windrichting:.0f}°"

    )
 
    draw.text((5, 5), text, inky.BLACK, font=font)

    inky.set_image(img)

    inky.show()
 
    # Sensor update en delay

    sensor.update(interval=5)

    time.sleep(10)
 
    # subprocess.run(["/bin", "/bin/auto_push.sh"])
 
    """

    repo_path = "/home/rpi/weatherhat-python/ICT-projecten/Programma"

    os.chdir(repo_path)

    os.system("git add .")

    os.system(f'git commit -m "auto"')

    os.system("git push origin main")

    """

 