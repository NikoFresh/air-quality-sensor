import time

import lib.adafruit_sgp30 as sgp30


class SGP30Sensor:
    def __init__(self, i2c):
        self.sgp30 = sgp30.Adafruit_SGP30(i2c)
        self.sgp30.iaq_init()
        print('Initializing SGP30...')
        time.sleep(15)
        print('SGP30 sensor initialized.')

    def read(self):
        co2_eq, tvoc = self.sgp30.iaq_measure()
        return {
            'eco2': co2_eq,
            'tvoc': tvoc,
        }
