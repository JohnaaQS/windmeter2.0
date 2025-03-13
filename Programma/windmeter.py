import RPi.GPIO as GPIO
import time
import math
import Adafruit_DHT

# Pinconfiguratie
sensorWindMeter = 3
dht_pin = 8
pulsen = 0
DiameterMagneetWindmeter = 0.03  # in meters
vorigeAantalMilliseconden = 0

# DHT instellen
DHT_SENSOR = Adafruit_DHT.DHT22  # Gebruik DHT11 of DHT22 afhankelijk van je sensor

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensorWindMeter, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Callback functie voor de interrupt
def teller(channel):
    global pulsen
    pulsen += 1

# Interrupt instellen
GPIO.add_event_detect(sensorWindMeter, GPIO.RISING, callback=teller)

def meet_wind_snelheid():
    global vorigeAantalMilliseconden, pulsen

    huidigeAantalMilliseconden = time.time() * 1000  # huidige tijd in ms
    if (huidigeAantalMilliseconden - vorigeAantalMilliseconden) >= 1000:  # elke seconde meten
        snelheid = math.pi * DiameterMagneetWindmeter * pulsen  # m/s
        snelheid_KM = snelheid * 3.6  # km/h
        print(f"De gemeten snelheid is: {snelheid:.2f} m/s")
        print(f"De gemeten snelheid is: {snelheid_KM:.2f} Km/H")
        
        # Reset pulsen voor de volgende meting
        pulsen = 0
        vorigeAantalMilliseconden = huidigeAantalMilliseconden

def meet_luchtvochtigheid_temperatuur():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, dht_pin)
    if humidity is not None and temperature is not None:
        print(f"Luchtvochtigheid: {humidity:.1f}%")
        print(f"Temperatuur: {temperature:.1f}°C")
    else:
        print("Fout bij het lezen van de DHT sensor")

try:
    while True:
        meet_wind_snelheid()
        meet_luchtvochtigheid_temperatuur()
        time.sleep(1)

except KeyboardInterrupt:
    print("Programma gestopt")

finally:
    GPIO.cleanup()
