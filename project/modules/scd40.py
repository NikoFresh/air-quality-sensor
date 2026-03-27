import lib.scd4x as scd4x


class SCD40Sensor:
    def __init__(self, i2c):
        self.scd = scd4x.SCD4X(i2c)
        self.scd.start_periodic_measurement()

    def read(self):
        return {
            'co2': self.scd.CO2
        }

    def set_pressure(self, pressure):
        self.scd.set_ambient_pressure(pressure)
