import lib.bme280_float as bme280


class BMESensor:
    def __init__(self, i2c):
        self.bme = bme280.BME280(i2c=i2c)
        print('BME sensor initialized.')

    def read(self):
        t, p, h = self.bme.values

        return {
            "temperature": t,
            "pressure": p,
            "humidity": h
        }
