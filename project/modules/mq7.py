from machine import Pin, ADC
import time
import math


class MQ7Sensor:
    VREF = 3.3
    ADC_MAX = 4095
    RL = 10.0

    # datasheet MQ7: CO ppm = a * (Rs/R0)^b
    CO_A = 99.042
    CO_B = -1.518

    # Warm-up
    WARMUP_MS = 180000

    def __init__(self, pin, r0=None):
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)

        self.r0 = r0  # if None start calibrating
        self._calibrated = r0 is not None
        self._warmup_start = time.ticks_ms()
        self._calibration_samples = []

        print('MQ7 sensor initialized. Warming up...')

    @property
    def is_warming_up(self):
        return time.ticks_diff(time.ticks_ms(), self._warmup_start) < self.WARMUP_MS

    def _read_rs(self):
        raw = self.adc.read()
        voltage = (raw / self.ADC_MAX) * self.VREF
        if voltage < 0.01:
            return None, raw, voltage
        rs = self.RL * (self.VREF - voltage) / voltage
        return rs, raw, voltage

    def _collect_calibration_sample(self, rs):
        self._calibration_samples.append(rs)
        if len(self._calibration_samples) > 10:
            self._calibration_samples.pop(0)

    def _finalize_calibration(self):
        if not self._calibration_samples:
            return
        self.r0 = sum(self._calibration_samples) / len(self._calibration_samples)
        self._calibrated = True
        print(f'MQ7 calibrated. R0 = {self.r0:.3f} kΩ')
        print(f'Puoi riusare questo valore: MQ7Sensor(pin=XX, r0={self.r0:.3f})')

    def read(self):
        rs, raw, voltage = self._read_rs()

        if self.is_warming_up:
            if rs is not None:
                self._collect_calibration_sample(rs)
            return {
                "mq7_raw": raw,
                "mq7_voltage": round(voltage, 3),
                "mq7_status": "warming_up",
                "mq7_co_ppm": None,
            }

        if not self._calibrated:
            self._finalize_calibration()

        if rs is None or self.r0 is None or self.r0 == 0:
            return {
                "mq7_raw": raw,
                "mq7_voltage": round(voltage, 3),
                "mq7_status": "error",
                "mq7_co_ppm": None,
            }

        # get ppm
        ratio = rs / self.r0
        ppm = self.CO_A * math.pow(ratio, self.CO_B)
        ppm = max(0, round(ppm, 1))

        return {
            "mq7_raw": raw,
            "mq7_voltage": round(voltage, 3),
            "mq7_rs": round(rs, 3),
            "mq7_ratio": round(ratio, 3),
            "mq7_status": "ok",
            "mq7_co_ppm": ppm,
        }
