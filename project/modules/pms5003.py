from machine import UART
import time


class PMS5003Sensor:
    START_BYTE_1 = 0x42
    START_BYTE_2 = 0x4D
    FRAME_LENGTH = 32

    def __init__(self, uart_id=1, tx=17, rx=16, baudrate=9600):
        self.uart = UART(uart_id, baudrate=baudrate, tx=tx, rx=rx,
                         bits=8, parity=None, stop=1)
        time.sleep_ms(100)
        print('PMS5003 sensor initialized.')

    def _read_frame(self):
        # find start byte of the buffer
        timeout = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), timeout) < 2000:
            if self.uart.any() >= self.FRAME_LENGTH:
                byte = self.uart.read(1)
                if byte and byte[0] == self.START_BYTE_1:
                    next_byte = self.uart.read(1)
                    if next_byte and next_byte[0] == self.START_BYTE_2:
                        # Leggi i restanti 30 bytes
                        rest = self.uart.read(30)
                        if rest and len(rest) == 30:
                            return bytes([self.START_BYTE_1, self.START_BYTE_2]) + rest
            time.sleep_ms(10)
        return None

    @staticmethod
    def _verify_checksum(frame):
        checksum = sum(frame[:30])
        received = (frame[30] << 8) | frame[31]
        return checksum == received

    def read(self):
        # empty buffer then read
        while self.uart.any():
            self.uart.read(self.uart.any())
        time.sleep_ms(800)

        frame = self._read_frame()
        if frame is None or not self._verify_checksum(frame):
            raise ValueError("PMS5003: frame non valido o checksum errato")

        return {
            "pm1_0":  (frame[4] << 8) | frame[5],   # PM1.0 µg/m³
            "pm2_5":  (frame[6] << 8) | frame[7],   # PM2.5 µg/m³
            "pm10":   (frame[8] << 8) | frame[9],   # PM10  µg/m³
            "pm1_0_atm": (frame[10] << 8) | frame[11],  # PM1.0 aria esterna
            "pm2_5_atm": (frame[12] << 8) | frame[13],  # PM2.5 aria esterna
            "pm10_atm":  (frame[14] << 8) | frame[15],  # PM10  aria esterna
        }
