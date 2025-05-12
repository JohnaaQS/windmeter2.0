import time
import csv
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from st7789 import ST7789
import weatherhat
import pygame
import threading

# Pygame setup (venster)
pygame.init()
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weerstation Dashboard")

# Kleuren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
BLUE = (100, 150, 255)
YELLOW = (255, 255, 100)
GREEN = (100, 255, 100)
GRAY = (200, 200, 200)

# Lettertype
font_large = pygame.font.SysFont("Arial", 36)
font_medium = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 22)

# Iconen laden
icon_paths = {
    "temperature": "icons/temperature.png",
    "humidity": "icons/humidity.png",
    "wind": "icons/wind.png",
    "light": "icons/light.png",
    "pressure": "icons/pressure.png"
}
icons = {key: pygame.image.load(path) for key, path in icon_paths.items()}

# LCD Display init
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

# Sensor init
sensor = weatherhat.WeatherHAT()

# CSV setup (eerste keer)
if not os.path.exists('weather_data.csv'):
    with open('weather_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tijdstip", "Apparaat Temperatuur (°C)", "Temperatuur (°C)",
                         "Luchtdruk (hPa)", "Luchtvochtigheid (%)", "Lichtintensiteit (lux)",
                         "Windsnelheid (m/s)", "Windrichting (graden)"])

def check_waarde(waarde):
    return "nvt" if waarde == 0 else round(waarde, 2)

# Fade-animatie
fade_alpha = 0
fade_direction = 1
fade_speed = 3

sensor_data = {}

def update_sensor_data():
    global sensor_data
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

        # LCD Output
        img = Image.new("RGB", (LCD_WIDTH, LCD_HEIGHT), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        message = f"Time: {tijdstip}\nWindrichting: {windrichting}°\nWindsnelheid: {windkracht} m/s\nTemp: {temperatuur}°C\nApparaat Temp: {apparaat_temperatuur}°C\nMade by JQS"
        draw.text((10, 10), message, font=font, fill=(255, 255, 255))
        disp.display(img)

        # CSV opslag
        with open('weather_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([tijdstip, apparaat_temperatuur, temperatuur,
                             druk, vochtigheid, lux, windkracht, windrichting])

        # Git push
        os.popen('/bin/auto_push.sh')

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

# Start sensor thread
threading.Thread(target=update_sensor_data, daemon=True).start()

# Hoofdlus voor Pygame
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    try:
        if sensor_data:
            screen.blit(font_large.render(f"Tijd: {sensor_data['tijd']}", True, WHITE), (40, 30))

            screen.blit(icons["temperature"], (40, 100))
            screen.blit(font_medium.render(f"{sensor_data['temperatuur']}°C", True, RED), (120, 110))

            screen.blit(icons["humidity"], (40, 170))
            screen.blit(font_medium.render(f"{sensor_data['vochtigheid']}%", True, BLUE), (120, 180))

            screen.blit(icons["wind"], (40, 240))
            screen.blit(font_medium.render(f"{sensor_data['windsnelheid']} m/s", True, GREEN), (120, 250))

            screen.blit(icons["pressure"], (40, 310))
            screen.blit(font_medium.render(f"{sensor_data['druk']} hPa", True, GRAY), (120, 320))

            screen.blit(icons["light"], (40, 380))
            screen.blit(font_medium.render(f"{sensor_data['licht']} lux", True, YELLOW), (120, 390))

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

