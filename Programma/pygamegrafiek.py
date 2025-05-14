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
    programma_map = "/home/rpi/weatherhat-python/ICT-projecten/Programma"
    file_path = os.path.join(programma_map, "weather_data.csv")
    os.makedirs("grafieken", exist_ok=True)
    df = pd.read_csv(file_path, header=0)

    df.columns = df.columns.str.strip()
    df.replace("nvt", np.nan, inplace=True)
    df.dropna(inplace=True)

    df["Tijdstip"] = pd.to_datetime(df["Tijdstip"], errors="coerce")
    df["Apparaat Temperatuur (\u00b0C)"] = pd.to_numeric(df["Apparaat Temperatuur (\u00b0C)"], errors="coerce")
    df["Temperatuur (\u00b0C)"] = pd.to_numeric(df["Temperatuur (\u00b0C)"], errors="coerce")
    df["Windsnelheid (m/s)"] = pd.to_numeric(df["Windsnelheid (m/s)"], errors="coerce")

    df = df.tail(400)

    plt.figure(figsize=(10, 5))
    plt.plot(df["Tijdstip"], df["Apparaat Temperatuur (\u00b0C)"], label="Apparaat Temp (\u00b0C)", color="red")
    plt.plot(df["Tijdstip"], df["Temperatuur (\u00b0C)"], label="Omgeving Temp (\u00b0C)", color="blue")
    plt.xlabel("Tijd")
    plt.ylabel("Temperatuur (\u00b0C)")
    plt.title("Temperatuurmetingen (0-50\u00b0C)")
    plt.ylim(0, 50)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("grafieken/temperatuur_grafiek.png", dpi=300)
    plt.show()
    time.sleep(10)
    plt.close()


    plt.figure(figsize=(10, 5))
    plt.plot(df["Tijdstip"], df["Windsnelheid (m/s)"], label="Windsnelheid (m/s)", color="purple")
    plt.xlabel("Tijd")
    plt.ylabel("Windsnelheid (m/s)")
    plt.title("Windsnelheidmetingen (0-20 m/s)")
    plt.ylim(0, 20)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("grafieken/windsnelheid_grafiek.png", dpi=300)
    plt.show()
    time.sleep(10)
    plt.close()

# Pygame setup
pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weerstation Dashboard")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
BLUE = (100, 150, 255)
YELLOW = (255, 255, 100)
GREEN = (100, 255, 100)
GRAY = (200, 200, 200)

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

# LCD init
SPI_SPEED_MHZ = 80
disp = ST7789(
    rotation=90,
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    spi_speed_hz=SPI_SPEED_MHZ * 1000 * 1000,
)
disp.begin()
LCD_WIDTH = disp.width
LCD_HEIGHT = disp.height
img = Image.new("RGB", (LCD_WIDTH, LCD_HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font_path = "/home/rpi/weatherhat-python/.venv/lib/python3.11/site-packages/font_manrope/files/Manrope-Bold.ttf"
font_size = 20
font = ImageFont.truetype(font_path, font_size)

sensor = weatherhat.WeatherHAT()

if not os.path.exists('weather_data.csv'):
    with open('weather_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tijdstip", "Apparaat Temperatuur (\u00b0C)", "Temperatuur (\u00b0C)",
                         "Luchtdruk (hPa)", "Luchtvochtigheid (%)", "Lichtintensiteit (lux)",
                         "Windsnelheid (m/s)", "Windrichting (graden)"])

def check_waarde(waarde):
    return "nvt" if waarde == 0 else round(waarde, 2)

sensor_data = {}

def update_sensor_data():
    global sensor_data
    laatste_opslaan = time.time()

    while True:
        tijdstip = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        apparaat_temperatuur = check_waarde(sensor.device_temperature)
        temperatuur = check_waarde(sensor.temperature)
        druk = check_waarde(sensor.pressure)
        vochtigheid = check_waarde(sensor.humidity)
        lux = check_waarde(sensor.lux)
        windkracht = check_waarde(sensor.wind_speed)
        windrichting = check_waarde(sensor.wind_direction)

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
                genereer_grafieken()
                print("Grafieken gegenereerd!")

    screen.blit(background, (0, 0))

    try:
        if sensor_data:
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

        pygame.draw.rect(screen, GREEN, button_rect)
        knop_tekst = font_small.render("Start Grafiek", True, BLACK)
        tekst_rect = knop_tekst.get_rect(center=button_rect.center)
        screen.blit(knop_tekst, tekst_rect)

        fade_alpha += fade_direction * fade_speed
        if fade_alpha >= 255:
            fade_alpha = 255
            fade_direction = -1
        elif fade_alpha <= 0:
            fade_alpha = 0
            fade_direction = 1

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
