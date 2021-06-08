#!/usr/bin/env python3

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
import logging
from suntime import Sun, SunTimeException
import time
from typing import List

from event import Emitter, Observer

env = None


class World:
    class Clock(Emitter):
        def __init__(self, timestep):
            super().__init__()
            self.time = datetime.now(timezone.utc)

        def tick(self):
            self.time += timedelta(minutes=1)
            self.notify(self.time)

    class Sun(Emitter, Observer):
        latitude = 51.21
        longitude = 21.01
        sun = Sun(latitude, longitude)

        def _sun_is_up(self, stime: datetime):
            return self.sun.get_sunrise_time(stime) < stime < self.sun.get_sunset_time(stime)

        def __init__(self, clock):
            super().__init__()
            self.logger = logging.getLogger(__class__.__name__)
            self.up = self._sun_is_up(clock.time)
            clock.attach(self)
            pass

        def update(self, stime: datetime):
            up = self._sun_is_up(stime)
            if up != self.up:
                self.logger.debug(f'The sun is {up=}')
                self.up = up
                self.notify(up)

    def __init__(self, timestep: timedelta):
        self.clock = self.Clock(timestep)
        self.sun = self.Sun(self.clock)
        pass
