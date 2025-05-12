"""
#runnen van therminal
sudo apt update
sudo apt install python3-pip
pip3 install pimoroni-bme280
pip3 install pimoroni-inky
python3 display_weather.py

"""


from bme280 import BME280
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw

# WeatherHAT setup
bme280 = BME280()
inky_display = InkyPHAT("black")

# Read sensor values
temperature = bme280.get_temperature()
pressure = bme280.get_pressure()
humidity = bme280.get_humidity()

# Create an image to display the data
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()

# Add sensor data to the image
draw.text((10, 10), f"Temp: {temperature:.1f} C", font=font, fill=inky_display.BLACK)
draw.text((10, 30), f"Pressure: {pressure:.1f} hPa", font=font, fill=inky_display.BLACK)
draw.text((10, 50), f"Humidity: {humidity:.1f} %", font=font, fill=inky_display.BLACK)

# Display the image on the screen
inky_display.set_image(img)
inky_display.show()
