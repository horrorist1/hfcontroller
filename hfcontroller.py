#!/usr/bin/env python3

import sensors
import logging


class HFController:
    light_sensor = None

    class TempSensor:
        pass

    class PresenceSensor:

        def on_presence(self):
            pass

    class TeachButton:

        def on_press(self):
            pass

    def __init__(self, has_window=True):
        super().__init__()
        self.logger = logging.getLogger(__class__.__name__)
        if has_window:
            self.light_sensor = sensors.LightSensor()
            self.light_sensor.attach(self)
        pass

    def update(self, data):
        if type(data) is bool:
            self.logger.info(f' light is {data}')

