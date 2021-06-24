#!/usr/bin/env python3

import sensors
import logging

import world
from humans import Pedant

from event import EventData


class HFController:
    class TempSensor:
        pass

    class PresenceSensor:

        def on_presence(self):
            pass

    class TeachButton:

        def on_press(self):
            pass

    def __init__(self, human: Pedant, has_window=True):
        super().__init__()
        self.logger = logging.getLogger(__class__.__name__)
        if has_window:
            self.light_sensor = sensors.LightSensor()
            self.light_sensor.attach(self)
        self.presence_sensor = sensors.PresenceSensor(human)
        self.presence_sensor.attach(self)

    def update(self, event: EventData):
        if type(event) is bool:
            self.logger.info(f' light is {event}')

