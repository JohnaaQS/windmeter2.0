import weatherhat
import time
from datetime import datetime
import csv
import subprocess

# De sensor initialiseren
sensor = weatherhat.WeatherHAT()

# GitHub uploadfunctie
def update_github_repo():
    try:
        # Voeg de wijzigingen toe aan git
        subprocess.run(["git", "add", "weather_data.csv"], check=True)

        # Commit de wijzigingen
        commit_message = f"Update weather data: {datetime.now().strftime('%d-%m-%y %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push de wijzigingen naar de repository
        subprocess.run(["git", "push"], check=True)

        print("Bestand succesvol naar GitHub gepusht.")
    except subprocess.CalledProcessError as e:
        print(f"Fout bij het updaten van de GitHub-repository: {e}")

# Maak CSV-bestand en schrijf de headers
with open('weather_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Tijdstip", "Apparaat Temperatuur (°C)", "Temperatuur (°C)",
                     "Luchtdruk (hPa)", "Luchtvochtigheid (%)", "Lichtintensiteit (lux)",
                     "Windsnelheid (m/s)", "Windrichting (graden)"])

while True:
    try:
        # Lees gegevens van de sensor
        apparaat_temperatuur = sensor.device_temperature
        temperatuur = sensor.temperature
        druk = sensor.pressure
        vochtigheid = sensor.humidity
        lux = sensor.lux
        windkracht = sensor.wind_speed
        windrichting = sensor.wind_direction

        # Print de waarden in de terminal
        tijdstip = datetime.now().strftime('%d-%m-%y %H:%M:%S')
        print(f"Tijdstip: {tijdstip}")
        print(f"Apparaat temperatuur: {apparaat_temperatuur:.2f} °C")
        print(f"Temperatuur: {temperatuur:.2f} °C")
        print(f"Luchtdruk: {druk:.2f} hPa")
        print(f"Luchtvochtigheid: {vochtigheid:.2f} %")
        print(f"Lichtintensiteit: {lux:.2f} lux")
        print(f"Windsnelheid: {windkracht:.2f} m/s")
        print(f"Windrichting: {windrichting:.2f} graden")

        # Schrijf de gegevens naar het CSV-bestand
        with open('weather_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([tijdstip, apparaat_temperatuur, temperatuur,
                             druk, vochtigheid, lux, windkracht, windrichting])

        # Upload naar GitHub
        update_github_repo()

        # Wacht 10 seconden voor de volgende update
        time.sleep(10)

    except Exception as e:
        fout_tijdstip = datetime.now().strftime('%d-%m-%y %H:%M:%S')
        print(f"Fout opgetreden op {fout_tijdstip}: {e}")
        time.sleep(5)  # Wacht even voordat je opnieuw probeert
