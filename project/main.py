from machine import Pin, I2C
import time
from modules.bme280 import BMESensor

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)

bme = BMESensor(i2c)

lastUpdateTime = time.ticks_ms()
interval = 2000
currentData = {}

while True:
    currTime = time.ticks_ms()
    if time.ticks_diff(currTime, lastUpdateTime) > interval:
        lastUpdateTime = currTime

        try:
            currentData.update(bme.read())
        except:
            print("Error")

        print(currentData)
        currentData = {}
