import weatherhat
import time

sensor = weatherhat.WeatherHAT()
while true:
 sensor.update(interval=5)
 time.sleep(1)


REFERENCE:
sensor.device_temprature
sensor.temprature
sensor.pressure
sensor.humidity
sensor.lux
sensor.wind
sensor.wind_direction