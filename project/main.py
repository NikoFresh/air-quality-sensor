from machine import Pin, I2C
import time
from modules.bme280 import BMESensor
from modules.sgp30 import SGP30Sensor
from modules.scd40 import SCD40Sensor
from modules.pms5003 import PMS5003Sensor
from modules.mq7 import MQ7Sensor

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)

bme = BMESensor(i2c)
sgp30 = SGP30Sensor(i2c)
scd = SCD40Sensor(i2c)
pms = PMS5003Sensor(uart_id=1, tx=17, rx=16)
mq7 = MQ7Sensor(pin=34, r0=1402.069)

lastUpdateTime = time.ticks_ms()
interval = 10000
currentData = {}

while True:
    currTime = time.ticks_ms()
    if time.ticks_diff(currTime, lastUpdateTime) > interval:
        lastUpdateTime = currTime

        try:
            currentData.update(bme.read())
            currentData.update(sgp30.read())  # According to docs we should read data only once every 60 seconds
            if currentData['pressure']:
                pressure = int(currentData['pressure'].split('.')[0])
                scd.set_pressure(pressure)
            currentData.update(scd.read())
            currentData.update(pms.read())
            currentData.update(mq7.read())
        except:
            print("Error")

        print(currentData)
        currentData = {}
