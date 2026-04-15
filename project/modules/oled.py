import lib.ssd1306 as ssd1306


class OLEDDisplay:
    def __init__(self, i2c, width=128, height=64):
        self.display = ssd1306.SSD1306_I2C(width, height, i2c)
        self.display.write_cmd(0xA0)
        self.display.write_cmd(0xC0)
        self._boot_screen()
        print('OLED display initialized.')

    def _boot_screen(self):
        self.display.fill(0)
        self.display.text("Caricamento...", 0, 0)
        self.display.hline(0, 10, 128, 1)
        self.display.show()

    def boot_add_sensor(self, sensors_so_far):
        self.display.fill(0)
        self.display.text("Caricamento...", 0, 0)
        self.display.hline(0, 10, 128, 1)
        y = 16
        for lbl, status in sensors_so_far:
            if status is None:
                icon = "..."
            elif status:
                icon = "OK "
            else:
                icon = "ERR"
            self.display.text(f"{lbl:<7} {icon}", 0, y)
            y += 9
        self.display.show()

    def update_data(self, data):
        self.display.fill(0)
        y_pos = 0

        wifi_status = "OK" if data.get('wifi_ok', False) else "NO"
        mqtt_status = "OK" if data.get('mqtt_ok', False) else "NO"
        self.display.text(f"WIFI:{wifi_status} MQTT:{mqtt_status}", 0, y_pos)
        self.display.hline(0, 10, 128, 1)
        y_pos += 15

        if 'co2' in data:
            self.display.text(f"CO2:   {data['co2']} ppm", 0, y_pos)
            y_pos += 10

        if 'tvoc' in data:
            self.display.text(f"TVOC:  {data['tvoc']} ppb", 0, y_pos)
            y_pos += 10

        if 'mq7_co_ppm' in data and data['mq7_co_ppm'] is not None:
            self.display.text(f"CO:    {data['mq7_co_ppm']} ppm", 0, y_pos)
            y_pos += 10

        if 'pm10_atm' in data and data['pm10_atm'] is not None:
            self.display.text(f"PM10:  {data['pm10_atm']} ug/m3", 0, y_pos)
            y_pos += 10

        if 'pm2_5_atm' in data and data['pm2_5_atm'] is not None:
            self.display.text(f"PM2.5: {data['pm2_5_atm']} ug/m3", 0, y_pos)
            y_pos += 10

        if 'pm1_0_atm' in data and data['pm1_0_atm'] is not None:
            self.display.text(f"PM1.0: {data['pm1_0_atm']} ug/m3", 0, y_pos)

        self.display.show()
