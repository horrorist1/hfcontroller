#!/usr/bin/env python3

from datetime import datetime
import world
from event import Emitter, Observer, EventData
import logging


class LightSensor(Emitter, Observer):
    def __init__(self):
        super().__init__()
        world.env.sun.attach(self)
        self.logger = logging.getLogger(__class__.__name__)
        pass

    def update(self, event: EventData):
        ct = world.env.clock.time
        self.logger.info(f'{ct}: {self.__class__.__name__} The sun is up: {event.data}')
        self.notify(event.data)
        pass


class PresenceSensor(Emitter, Observer):
    def __init__(self):
        super().__init__()

    def update(self, data):
        pass

