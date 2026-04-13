import lib.ssd1306 as ssd1306

class OLEDDisplay:
    def __init__(self, i2c, width=128, height=64):
        self.display = ssd1306.SSD1306_I2C(width, height, i2c)
        # Rotate screen
        self.display.write_cmd(0xA0)  # SEG remap
        self.display.write_cmd(0xC0)  # COM output direction

        self.display.fill(0)
        self.display.text("Avvio sensori...", 0, 28)
        self.display.show()
        print('OLED display initialized.')

    def update_data(self, data):
        self.display.fill(0)
        y_pos = 0

        wifi_status = "OK" if data.get('wifi_ok', False) else "NO"
        mqtt_status = "OK" if data.get('mqtt_ok', False) else "NO"
        self.display.text(f"WIFI:{wifi_status} MQTT:{mqtt_status}", 0, y_pos)
        y_pos += 9

        if 'co2' in data:
            self.display.text(f"CO2:  {data['co2']} ppm", 0, y_pos)
            y_pos += 9

        if 'tvoc' in data:
            self.display.text(f"TVOC: {data['tvoc']} ppb", 0, y_pos)
            y_pos += 9

        if 'mq7_co_ppm' in data and data['mq7_co_ppm'] is not None:
            self.display.text(f"CO:   {data['mq7_co_ppm']} ppm", 0, y_pos)
            y_pos += 9

        if 'pm10_atm' in data and data['pm10_atm'] is not None:
            self.display.text(f"PM10: {data['pm10_atm']} ug/m3", 0, y_pos)
            y_pos += 9

        if 'pm2_5_atm' in data and data['pm2_5_atm'] is not None:
            self.display.text(f"PM2.5:{data['pm2_5_atm']} ug/m3", 0, y_pos)
            y_pos += 9

        if 'pm1_0_atm' in data and data['pm1_0_atm'] is not None:
            self.display.text(f"PM1.0:{data['pm1_0_atm']} ug/m3", 0, y_pos)

        self.display.show()
