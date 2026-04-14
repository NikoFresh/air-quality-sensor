from machine import Pin, I2C
import time
import network
from modules.bme280 import BMESensor
from modules.sgp30 import SGP30Sensor
from modules.scd40 import SCD40Sensor
from modules.pms5003 import PMS5003Sensor
from modules.mq7 import MQ7Sensor
from modules.oled import OLEDDisplay
from modules.mqtt import connect_wifi, MQTTManager

# Hardware
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)

oled = OLEDDisplay(i2c)
bme = BMESensor(i2c)
sgp = SGP30Sensor(i2c)
scd = SCD40Sensor(i2c)
pms = PMS5003Sensor(uart_id=1, tx=17, rx=16)
# mq7 = MQ7Sensor(pin=34, r0=1402.069)

connect_wifi()
mqtt = MQTTManager()

# Intervals (ms)
SGP30_INTERVAL = 1_000
SCD40_INTERVAL = 5_000
BME_INTERVAL = 10_000
MQ7_INTERVAL = 10_000
PMS_INTERVAL = 30_000
OLED_INTERVAL = 5_000
PUBLISH_INTERVAL = 30_000

now = time.ticks_ms()
last_sgp30 = now
last_scd40 = now
last_bme = now
last_mq7 = now
last_pms = now
last_oled = now
last_publish = now

data = {}
while True:
    now = time.ticks_ms()

    wlan = network.WLAN(network.STA_IF)
    wifi_connected = wlan.isconnected()

    if wifi_connected:
        mqtt_ok = mqtt.check_connection()
    else:
        mqtt.clients = []
        mqtt_ok = False

    # SGP30
    if time.ticks_diff(now, last_sgp30) >= SGP30_INTERVAL:
        last_sgp30 = now
        try:
            sgp_data = sgp.read()
            if 'eco2' in sgp_data:
                sgp_data['eco2'] = sgp_data.pop('eco2')
            data.update(sgp_data)
        except Exception as e:
            print("[SGP30] errore:", e)

    # SCD40
    if time.ticks_diff(now, last_scd40) >= SCD40_INTERVAL:
        last_scd40 = now
        try:
            pressure_str = data.get('pressure')
            if pressure_str:
                scd.set_pressure(int(pressure_str.split('.')[0]))
            data.update(scd.read())
        except Exception as e:
            print("[SCD40] errore:", e)

    # BME280
    if time.ticks_diff(now, last_bme) >= BME_INTERVAL:
        last_bme = now
        try:
            data.update(bme.read())
        except Exception as e:
            print("[BME280] errore:", e)

    # MQ7
    # if time.ticks_diff(now, last_mq7) >= MQ7_INTERVAL:
    #     last_mq7 = now
    #     try:
    #         data.update(mq7.read())
    #     except Exception as e:
    #         print("[MQ7] errore:", e)

    # PMS5003
    if time.ticks_diff(now, last_pms) >= PMS_INTERVAL:
        last_pms = now
        try:
            data.update(pms.read())
        except Exception as e:
            print("[PMS5003] errore:", e)

    # OLED
    if time.ticks_diff(now, last_oled) >= OLED_INTERVAL:
        last_oled = now
        wlan = network.WLAN(network.STA_IF)
        data['wifi_ok'] = wlan.isconnected()
        data['mqtt_ok'] = len(mqtt.clients) > 0
        if data:
            oled.update_data(data)

    # MQTT
    if time.ticks_diff(now, last_publish) >= PUBLISH_INTERVAL:
        last_publish = now
        if data and wifi_connected and mqtt_ok:
            mqtt.publish(data)
            print(data)

    time.sleep_ms(50)
