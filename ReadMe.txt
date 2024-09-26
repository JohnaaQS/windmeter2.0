Vereisten:
Installeer de benodigde Python-bibliotheken:

bash
Code kopiëren:
pip install RPi.GPIO spidev smbus2

Zorg ervoor dat de sensorbestanden en GPIO-instellingen correct zijn geconfigureerd voor de Raspberry Pi.


installeer de benodigde Python-bibliotheken: pip install RPi.GPIO spidev smbus2
Uitleg:
read_windsnelheid, read_windrichting, en read_regenval zijn voorbeeldfuncties die sensorwaarden teruggeven. Je moet deze functies aanpassen om daadwerkelijk de gegevens van je specifieke sensoren uit te lezen.
Het programma slaat de gemeten gegevens elke minuut op en schrijft de data naar een CSV-bestand na X aantal metingen.
GPIO.cleanup() zorgt ervoor dat de gebruikte pinnen worden vrijgegeven als het programma stopt.
CSV-bestand:
Het programma maakt of vult een CSV-bestand met de volgende velden:

Tijdstip: Het tijdstip van de meting.
Windsnelheid: De gemeten windsnelheid.
Windrichting: De gemeten windrichting.
Regenval: De gemeten regenval.



### Wat is een CSV-bestand?

Een **CSV-bestand** (*Comma-Separated Values*) is een tekstbestand waarin gegevens in tabellen worden opgeslagen. Elke rij in de tabel is een nieuwe regel in het bestand, en de waarden in elke rij worden gescheiden door komma's (of soms andere scheidingstekens, zoals puntkomma's). Dit formaat wordt veel gebruikt voor het opslaan van gestructureerde gegevens, zoals spreadsheetgegevens, en kan door programma's zoals Microsoft Excel, Google Sheets en veel databases worden geopend.

Hier is een voorbeeld van hoe een CSV-bestand eruit kan zien:

```csv
Tijdstip,Windsnelheid,Windrichting,Regenval
2024-09-19 10:00:00,5.2,180,0.3
2024-09-19 11:00:00,6.1,200,0.5
2024-09-19 12:00:00,7.4,170,0.0
```

### Waar vind je de sensorwaardes?

Voor de Raspberry Pi en de specifieke sensoren (**Weather HAT** en **SparkFun Weather Shield**), moet je de sensorgegevens via de GPIO-pinnen uitlezen, en de gebruikte bibliotheken zullen afhankelijk zijn van welke sensor je hebt.

#### 1. **Weather HAT**:
   De **Weather HAT** van Pimoroni bevat verschillende sensoren, waaronder voor windsnelheid, windrichting en regenval. Om deze waarden uit te lezen, kun je gebruikmaken van de bijbehorende Python-bibliotheek van Pimoroni.

   - **Installeren van de Weather HAT-bibliotheek**:
     Als je de officiële Pimoroni Python-bibliotheek gebruikt, installeer je deze met het volgende commando:
     ```bash
     pip install pimoroni-weatherhat
     ```

   - **Voorbeeld voor het uitlezen van sensorgegevens**:
     ```python
     from weatherhat import WeatherHAT
     
     weatherhat = WeatherHAT()

     # Lees windsnelheid
     windsnelheid = weatherhat.wind_speed()

     # Lees windrichting
     windrichting = weatherhat.wind_direction()

     # Lees regenval
     regenval = weatherhat.rain()
     ```

   Deze waarden kun je dan gebruiken in het programma dat ik eerder gaf.

#### 2. **SparkFun Weather Shield**:
   Het **SparkFun Weather Shield** werkt met een I2C-interface en vereist ook een bibliotheek om de gegevens uit te lezen. Deze kan via sensoren zoals de **anemometer** (voor windsnelheid) en **regenmeter** aangesloten zijn.

   - **Bibliotheek voor SparkFun Weather Shield**:
     Als je de SparkFun-bibliotheken voor Python gebruikt, installeer je deze met de volgende commando's:
     ```bash
     pip install sparkfun-qwiic
     ```

   - **Voorbeeld voor het uitlezen van sensorgegevens**:
     Voor het uitlezen van de gegevens van de SparkFun Weather Shield, gebruik je hun `Qwiic` bibliotheek om data van de aangesloten sensoren te verkrijgen. 

   Raadpleeg de specifieke SparkFun-documentatie voor meer details over de exacte functies en variabelen om de waarden te verkrijgen, afhankelijk van de aangesloten sensoren.

### Samenvatting:
1. **CSV-bestanden** zijn eenvoudig te openen en te bewerken in programma's zoals Excel en worden vaak gebruikt voor het opslaan van gestructureerde gegevens.
2. Je kunt de sensordata van de **Weather HAT** en **SparkFun Weather Shield** verkrijgen via hun respectieve Python-bibliotheken, die toegang geven tot windsnelheid, windrichting en regenval.

Als je hulp nodig hebt met specifieke sensoren of details, laat het me weten!