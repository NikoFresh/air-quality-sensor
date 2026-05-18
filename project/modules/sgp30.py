import time

import lib.adafruit_sgp30 as sgp30


class SGP30Sensor:
    def __init__(self, i2c):
        self.sgp30 = sgp30.Adafruit_SGP30(i2c)
        self.sgp30.iaq_init()
        print('Initializing SGP30...')
        # time.sleep(15)
        # print('SGP30 sensor initialized.')

    def set_humidity(self, temperature, humidity):
        try:
            # g/m³ = (RH/100) * 6.112 * exp(17.67*T/(T+243.5)) * 216.7/(T+273.15)
            import math
            abs_hum = (humidity / 100.0) * 6.112 * math.exp(
                17.67 * temperature / (temperature + 243.5)
            ) * 216.7 / (temperature + 273.15)
            abs_hum_fp = int(abs_hum) << 8 | int((abs_hum % 1) * 256)
            self.sgp30.set_iaq_humidity(abs_hum_fp)
        except Exception as e:
            print("SGP30: set_humidity:", e)

    def read(self):
        co2_eq, tvoc = self.sgp30.iaq_measure()
        return {
            'eco2': co2_eq,
            'tvoc': tvoc,
        }
