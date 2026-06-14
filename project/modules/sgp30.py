import lib.uSGP30 as uSGP30


class SGP30Sensor:
    def __init__(self, i2c):
        self.sgp30 = uSGP30.SGP30(i2c)
        print('Initializing SGP30...')
        self.sgp30.iaq_init()

    def _parse_number(self, val):
        if isinstance(val, str):
            clean_str = "".join([c for c in val if c.isdigit() or c in '.-'])
            return float(clean_str) if clean_str else 0.0
        return float(val)

    def set_humidity(self, temp, hum):
        clean_temp = self._parse_number(temp)
        clean_hum = self._parse_number(hum)
        a_hum = uSGP30.convert_r_to_a_humidity(clean_temp, clean_hum)
        self.sgp30.set_absolute_humidity(a_hum)

    def read(self):
        co2_eq, tvoc = self.sgp30.measure_iaq()
        return {
            'eco2': co2_eq,
            'tvoc': tvoc,
        }
