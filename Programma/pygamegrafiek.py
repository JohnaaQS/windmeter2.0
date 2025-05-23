import time
import csv
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from st7789 import ST7789
import weatherhat
import pygame
import threading
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Functie voor grafieken genereren
def genereer_grafieken():
    #juiste map en bestand vinden 
    programma_map = "/home/rpi/weatherhat-python/ICT-projecten/Programma"
    file_path = os.path.join(programma_map, "weather_data.csv")
    os.makedirs("grafieken", exist_ok=True)
    df = pd.read_csv(file_path, header=0)

    #vervangt nvt door een onbestaand getal en verwijder heet 
    df.columns = df.columns.str.strip()
    df.replace("nvt", np.nan, inplace=True)  
    df.dropna(inplace=True)
    
    #omvormen naar juiste datatypes 
    df["Tijdstip"] = pd.to_datetime(df["Tijdstip"], errors="coerce")
    df["Apparaat Temperatuur (°C)"] = pd.to_numeric(df["Apparaat Temperatuur (°C)"], errors="coerce")
    df["Temperatuur (°C)"] = pd.to_numeric(df["Temperatuur (°C)"], errors="coerce")
    df["Windsnelheid (m/s)"] = pd.to_numeric(df["Windsnelheid (m/s)"], errors="coerce")
    df["Lichtintensiteit (lux)"] = pd.to_numeric(df["Lichtintensiteit (lux)"], errors="coerce")
    
    #df = df.head(600)
    df = df.tail(400) # zo pak je alleen de laatste 400
   
    ## zo pak je een bepaald stuk eruit##
    #df = df.head(200:400)
    
    
    ###TEMPERATUREN###
    plt.figure(figsize=(10, 5))
    plt.plot(df["Tijdstip"], df["Apparaat Temperatuur (°C)"], label="Apparaat Temp (°C)", color="red")
    plt.plot(df["Tijdstip"], df["Temperatuur (°C)"], label="Omgeving Temp (°C)", color="blue")
    
    plt.xlabel("Tijd")
    plt.ylabel("Temperatuur (°C)")
    plt.title("Temperatuurmetingen (0-50°C)")
    plt.ylim(0, 50)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    
    plt.savefig("grafieken/temperatuur_grafiek.png", dpi=300)
    print("Grafiek opgeslagen: temperatuur_grafiek.png")
    plt.show()
    
    
    ###WINDSNELHEID###
    plt.figure(figsize=(10, 5))
    plt.plot(df["Tijdstip"], df["Windsnelheid (m/s)"], label="Windsnelheid (m/s)", color="purple")
    
    plt.xlabel("Tijd")
    plt.ylabel("Windsnelheid (m/s)")
    plt.title("Windsnelheidmetingen (0-20 m/s)")
    plt.ylim(0, 20)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    
    plt.savefig("grafieken/windsnelheid_grafiek.png", dpi=300)
    plt.show()
    
    
    ###LICHTINTENSITEIT###
    plt.figure(figsize=(10, 5))
    plt.plot(df["Tijdstip"], df["Lichtintensiteit (lux)"], label="Lichtintensiteit (lux)", color="orange")
    
    plt.xlabel("Tijd")
    plt.ylabel("Lichtintensiteit (lux)")
    plt.title("Lichtintensiteitmetingen (0-1000 lux)")
    plt.ylim(0, 1000)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    
    plt.savefig("grafieken/lichtintensiteit_grafiek.png", dpi=300)
    plt.show()


# Pygame setup
pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weerstation Dashboard")

#Kleurcodes 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
BLUE = (100, 150, 255)
YELLOW = (255, 255, 100)
GREEN = (100, 255, 100)
GRAY = (200, 200, 200)

#lettertypes 
font_large = pygame.font.SysFont("Arial", 36)
font_medium = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 22)

# Iconen
icon_paths = {
    "temperature": "icons/temperature.png",
    "humidity": "icons/humidity.png",
    "wind": "icons/wind.png",
    "light": "icons/light.png",
    "pressure": "icons/pressure.png"
}

icons = {}
for key, path in icon_paths.items():
    try:
        icon = pygame.image.load(path)
        icons[key] = pygame.transform.scale(icon, (40, 40))
    except Exception as e:
        print(f"Fout bij laden van icoon '{path}': {e}")

# === TOEGEVOEGD: Windrichting-pijl laden ===
try:
    arrow_image = pygame.image.load("icons/arrow.png")
    arrow_image = pygame.transform.scale(arrow_image, (50, 50))
except Exception as e:
    print(f"Fout bij laden van pijl icoon: {e}")
    arrow_image = None

# LCD instellingen 
SPI_SPEED_MHZ = 80
disp = ST7789(
    rotation=90,
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    spi_speed_hz=SPI_SPEED_MHZ * 1000 * 1000,
)
#display start
disp.begin()
LCD_WIDTH = disp.width
LCD_HEIGHT = disp.height
img = Image.new("RGB", (LCD_WIDTH, LCD_HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font_path = "/home/rpi/weatherhat-python/.venv/lib/python3.11/site-packages/font_manrope/files/Manrope-Bold.ttf"
font_size = 20
font = ImageFont.truetype(font_path, font_size)

sensor = weatherhat.WeatherHAT()

with open('weather_data.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Tijdstip", "Apparaat Temperatuur (°C)", "Temperatuur (°C)",
                     "Luchtdruk (hPa)", "Luchtvochtigheid (%)", "Lichtintensiteit (lux)",
                     "Windsnelheid (m/s)", "Windrichting (graden)"])

#waarde omvormen naar 0 & afronden tot 2 na de komma
def check_waarde(waarde):
    return "nvt" if waarde == 0 else round(waarde, 2)

sensor_data = {}

def update_sensor_data():
    #tijd bijhouden 
    global sensor_data
    laatste_opslaan = time.time()

    while True:
        #uitlezen van sensor en evt. waardes omvormen bij 0 waarden 
        tijdstip = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        apparaat_temperatuur = check_waarde(sensor.device_temperature)
        temperatuur = check_waarde(sensor.temperature)
        druk = check_waarde(sensor.pressure)
        vochtigheid = check_waarde(sensor.humidity)
        lux = check_waarde(sensor.lux)
        windkracht = check_waarde(sensor.wind_speed)
        windrichting = sensor.wind_direction

        # Console output
        print(f"Tijd: {tijdstip}")
        print(f"Apparaat Temp: {apparaat_temperatuur} °C")
        print(f"Temperatuur: {temperatuur} °C")
        print(f"Luchtdruk: {druk} hPa")
        print(f"Luchtvochtigheid: {vochtigheid} %")
        print(f"Lichtintensiteit: {lux} lux")
        print(f"Windsnelheid: {windkracht} m/s")
        print(f"Windrichting: {windrichting} graden")
        print("------------------------------------")

        # LCD display update
        img = Image.new("RGB", (LCD_WIDTH, LCD_HEIGHT), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        message = f"Time: {tijdstip}\nWindrichting: {windrichting}\u00b0\nWindsnelheid: {windkracht} m/s\nTemp: {temperatuur}\u00b0C\nApparaat Temp: {apparaat_temperatuur}\u00b0C\nMade by JQS"
        draw.text((10, 10), message, font=font, fill=(255, 255, 255))
        disp.display(img)

        # Alleen opslaan naar CSV elke 60 seconden
        nu = time.time()
        if nu - laatste_opslaan >= 60:
            with open('weather_data.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([tijdstip, apparaat_temperatuur, temperatuur,
                                druk, vochtigheid, lux, windkracht, windrichting])
                print("Gegevens opgeslagen in CSV.")

            #gegevens naar github sturen 
            os.popen('/bin/auto_push.sh')
            print("Git push succesvol!")

            laatste_opslaan = nu

        sensor_data = {
            "tijd": tijdstip,
            "temperatuur": temperatuur,
            "apparaat_temp": apparaat_temperatuur,
            "vochtigheid": vochtigheid,
            "druk": druk,
            "licht": lux,
            "windsnelheid": windkracht,
            "windrichting": windrichting
        }

        sensor.update(interval=5)
        time.sleep(10)

threading.Thread(target=update_sensor_data, daemon=True).start()

background = pygame.image.load("icons/backgroundwm.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

button_rect = pygame.Rect(WIDTH - 200, 30, 150, 50)
fade_alpha = 0
fade_direction = 1
fade_speed = 3
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print("Knop ingedrukt!")
                genereer_grafieken()
                print("Grafieken gegenereerd!")

    screen.blit(background, (0, 0))

    try: 
        if sensor_data:
            #sensor waardes printen in het pygame venster
            screen.blit(font_large.render(f"Tijd: {sensor_data['tijd']}", True, WHITE), (40, 30))
            screen.blit(icons["temperature"], (40, 100))
            screen.blit(font_medium.render(f"{sensor_data['temperatuur']}\u00b0C", True, BLACK), (120, 110))
            screen.blit(icons["humidity"], (40, 160))
            screen.blit(font_medium.render(f"{sensor_data['vochtigheid']}%", True, BLACK), (120, 170))
            screen.blit(icons["wind"], (40, 220))
            screen.blit(font_medium.render(f"{sensor_data['windsnelheid']} m/s", True, BLACK), (120, 230))
            screen.blit(icons["wind"], (40, 280))
            screen.blit(font_medium.render(f"{sensor_data['windrichting']}\u00b0", True, BLACK), (120, 290))
            screen.blit(icons["pressure"], (40, 340))
            screen.blit(font_medium.render(f"{sensor_data['druk']} hPa", True, BLACK), (120, 350))
            screen.blit(icons["light"], (40, 400))
            screen.blit(font_medium.render(f"{sensor_data['licht']} lux", True, BLACK), (120, 410))

            #pijl voor windrichting 
            if arrow_image and "windrichting" in sensor_data:
                hoek = -sensor_data["windrichting"]
                gedraaide_pijl = pygame.transform.rotate(arrow_image, hoek)
                pijl_rect = gedraaide_pijl.get_rect(center=(700, 180))
                screen.blit(gedraaide_pijl, pijl_rect)
                # Kompasletters (N, O, Z, W)
                
                richtingen = {
                    "N": (pijl_rect.centerx, pijl_rect.top - 30),
                    "O": (pijl_rect.right + 20, pijl_rect.centery),
                    "Z": (pijl_rect.centerx, pijl_rect.bottom + 30),
                    "W": (pijl_rect.left - 20, pijl_rect.centery),
                }

                for letter, pos in richtingen.items():
                    tekst = font_small.render(letter, True, WHITE)
                    tekst_rect = tekst.get_rect(center=pos)
                    screen.blit(tekst, tekst_rect)
                
        #grafiekknop aanmaken 
        pygame.draw.rect(screen, GREEN, button_rect)
        knop_tekst = font_small.render("Start Grafiek", True, BLACK)
        tekst_rect = knop_tekst.get_rect(center=button_rect.center)
        screen.blit(knop_tekst, tekst_rect)
                
        #grafiekknop aanmaken 
        pygame.draw.rect(screen, GREEN, button_rect)
        knop_tekst = font_small.render("Start Grafiek", True, BLACK)
        tekst_rect = knop_tekst.get_rect(center=button_rect.center)
        screen.blit(knop_tekst, tekst_rect)

        #text fade 
        fade_alpha += fade_direction * fade_speed
        if fade_alpha >= 255:
            fade_alpha = 255
            fade_direction = -1
        elif fade_alpha <= 0:
            fade_alpha = 0
            fade_direction = 1

        #watermark by JQS
        fade_surface = font_small.render("Made by JQS", True, WHITE)
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (WIDTH - 200, HEIGHT - 50))

    except Exception as e:
        print("Fout bij tekenen pygame:", e)

    pygame.display.flip()
    clock.tick(1)

pygame.quit()
disp.set_backlight(0)
print("Programma afgesloten")
