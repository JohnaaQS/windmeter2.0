import weatherhat
import time
from datetime import datetime
import csv
import pygame

#de sensor
sensor = weatherhat.WeatherHAT()

#pygame instellingen 
pygame.init()
width, height = 600, 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Weergave weersomstandigheden")
font = pygame.font.Font(None, 30)


with open('weather_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Tijdstip", "Apparaat Temperatuur (°C)", "Temperatuur (°C)",
                     "Luchtdruk (hPa)", "Luchtvochtigheid (%)", "Lichtintensiteit (lux)", 
                     "Windsnelheid (m/s)", "Windrichting (graden)"])

running = True
refresh_time = 3  # ververstijd in seconden
last_update = time.time() - refresh_time 

while running:
    for event in pygame.event.get():
        
     if event.type == pygame.QUIT:
         running = False

    try:
        # Lees sensor uit
        apparaat_temperatuur = sensor.device_temperature
        temperatuur = sensor.temperature
        druk = sensor.pressure
        vochtigheid = sensor.humidity
        lux = sensor.lux
        windkracht = sensor.wind_speed
        windrichting = sensor.wind_direction

        # Print de waarden in de therminal
        tijdstip = datetime.now().strftime('%d-%m-%y %H:%M:%S')
        print(f"Tijdstip: {tijdstip}")
        print(f"Apparaat temperatuur: {apparaat_temperatuur:.2f} °C")
        print(f"Temperatuur: {temperatuur:.2f} °C")
        print(f"Luchtdruk: {druk:.2f} hPa")
        print(f"Luchtvochtigheid: {vochtigheid:.2f} %")
        print(f"Lichtintensiteit: {lux:.2f} lux")
        print(f"Windsnelheid: {windkracht:.2f} m/s")
        print(f"Windrichting: {windrichting:.2f} graden")
          
        #wegschrijven van de data    
        with open('weather_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now(), apparaat_temperatuur, temperatuur, 
                         druk, vochtigheid, lux, windkracht, windrichting])
        
        window.fill((255, 255, 255))  
        tijd_text = font.render(f"Tijdstip: {tijdstip}", True, (0, 0, 0))
        apparaat_temperatuur_text = font.render(f"Apparaat temperatuur: {apparaat_temperatuur}", True, (0, 0, 0))
        temperatuur_text = font.render(f"Temperatuur: {temperatuur}", True, (0, 0, 0))
        Luchtdruk_text = font.render(f"Luchtdruk: {druk}", True, (0, 0, 0))
        Luchtvochtigheid_text = font.render(f"Luchtvochtigheid: {vochtigheid}", True, (0, 0, 0))
        Lichtintensiteit_text = font.render(f"Lichtintensiteit: {lux}", True, (0, 0, 0))
        Windsnelheid_text = font.render(f"Windsnelheid: {windkracht}", True, (0, 0, 0))
        Windrichting_text = font.render(f"Windrichting: {windrichting}", True, (0, 0, 0))
        
        window.blit(tijd_text, (10, 10))
        window.blit(apparaat_temperatuur_text, (10, 70))
        window.blit(temperatuur_text, (10, 130))
        window.blit(Luchtdruk_text, (10, 190))
        window.blit(Luchtvochtigheid_text, (10, 250))
        window.blit(Lichtintensiteit_text, (10, 310))
        window.blit(Windsnelheid_text, (10, 370))
        window.blit(Windrichting_text, (10, 430))
        
        pygame.display.flip()

        # Wacht 10 seconden
        time.sleep(10)

    except Exception as e:
        fout_tijdstip = datetime.now().strftime('%d-%m-%y %H:%M:%S')
        print(f"Fout opgetreden op {fout_tijdstip}: {e}")
        time.sleep(5)  # Wacht even voordat je opnieuw probeert
    pygame.display.update()
    
pygame.quit()