#!/usr/bin/env python3

from datetime import datetime
import world
from event import Emitter, Observer
import logging


class LightSensor(Emitter, Observer):
    def __init__(self):
        super().__init__()
        world.env.sun.attach(self)
        self.logger = logging.getLogger(__class__.__name__)
        pass

    def update(self, up):
        self.logger.debug(f' {world.env.clock.time}The sun is up: {up}')
        self.notify(up)
        pass


class PresenceSensor(Emitter, Observer):
    def __init__(self):
        super().__init__()

    def update(self, data):
        pass

