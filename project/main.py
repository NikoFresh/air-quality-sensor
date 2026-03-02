from machine import Pin, I2C
import time
from modules.bme280 import BMESensor
from modules.sgp30 import SGP30Sensor

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)

bme = BMESensor(i2c)
sgp30 = SGP30Sensor(i2c)

lastUpdateTime = time.ticks_ms()
interval = 2000
currentData = {}

while True:
    currTime = time.ticks_ms()
    if time.ticks_diff(currTime, lastUpdateTime) > interval:
        lastUpdateTime = currTime

        try:
            currentData.update(bme.read())
            currentData.update(sgp30.read()) # According to docs we should read data only once every 60 seconds
        except:
            print("Error")

        print(currentData)
        currentData = {}
