import weatherhat 
import time
import csv
from datetime import datetime
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw

sensor = weatherhat.WeatherHAT()
inky_display = InkyPHAT("black")

with open('weather_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Tijdstip", "Apparaat Temperatuur (°C)", "Temperatuur (°C)",
                     "Luchtdruk (hPa)", "Luchtvochtigheid (%)", "Lichtintensiteit (lux)", 
                     "Windsnelheid (m/s)", "Windrichting (graden)"])

while True:
 apparaat_temperatuur = sensor.device_temperature 
 tempratuur = sensor.temperature
 druk = sensor.pressure
 vochtigheid = sensor.humidity
 lux = sensor.lux
 windkracht = sensor.wind_speed
 windrichting = sensor.wind_direction
 
 
 print(f"Apparaat temperatuur: {apparaat_temperatuur:.2f} °C")
 
 print(f"temperatuur: {tempratuur:.2f}")
 
 print(f"luchtdruk: {druk:.2f} hPa")
 
 print(f"Luchtvochtigheid: {vochtigheid:.2f} %")
 
 print(f"Lichtintensiteit: {lux:.2f} lux")
 
 print(f"Windsnelheid: {windkracht:.2f} m/s")
 
 print(f"Windrichting: {windrichting:.2f} graden")
 
 
 with open('weather_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), apparaat_temperatuur, tempratuur, 
                         druk, vochtigheid, lux, windkracht, windrichting])
        
 # Scherm aansturen
 img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
 draw = ImageDraw.Draw(img)
 font = ImageFont.load_default()

 # Tekst toevoegen aan het beeld
 draw.text((10, 10), f"App. temp: {apparaat_temperatuur:.2f} C", font=font, fill=inky_display.BLACK)
 draw.text((10, 30), f"Temp: {tempratuur:.2f} C", font=font, fill=inky_display.BLACK)
 draw.text((10, 50), f"Druk: {druk:.2f} hPa", font=font, fill=inky_display.BLACK)
 draw.text((10, 70), f"Vochtigheid: {vochtigheid:.2f} %", font=font, fill=inky_display.BLACK)
 draw.text((10, 90), f"Licht: {lux:.2f} lux", font=font, fill=inky_display.BLACK)
 draw.text((10, 110), f"Wind: {windkracht:.2f} m/s", font=font, fill=inky_display.BLACK)
 draw.text((10, 130), f"Windricht.: {windrichting:.2f} graden", font=font, fill=inky_display.BLACK)

 # Beeld op het scherm tonen
 inky_display.set_image(img)
 inky_display.show()
        
 
 sensor.update(interval=5)
 time.sleep(10)
 
