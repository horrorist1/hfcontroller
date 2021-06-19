#!/usr/bin/env python3

from datetime import datetime, timedelta, date
import logging
from suntime import Sun
import pytz

from event import Emitter, Observer, EventData

env = None

latitude = 59.92107162856273
longitude = 30.343245379259553


class World:
    class Clock(Emitter):
        timezone = pytz.timezone('Europe/Moscow')

        def __init__(self, timestep):
            super().__init__()
            self.time = datetime.combine(date.today(), datetime.min.time(), tzinfo=World.Clock.timezone)

        def tick(self):
            self.time += timedelta(minutes=1)
            self.notify(self.time)

    class Sun(Emitter, Observer):
        sun = Sun(latitude, longitude)

        def _sun_is_up(self, stime: datetime):
            return self.sun.get_local_sunrise_time(stime) < stime < self.sun.get_local_sunset_time(stime)

        def __init__(self, clock):
            super().__init__()
            self.logger = logging.getLogger(__class__.__name__)
            self.up = self._sun_is_up(clock.time)
            clock.attach(self)
            pass

        def update(self, data: EventData):
            up = self._sun_is_up(data.data)
            if up != self.up:
                ct = env.clock.time
                self.logger.debug(f'{ct.year}.{ct.month}.{ct.day} {ct.hour}:{ct.minute}: The sun is {up}')
                self.up = up
                self.notify(up)

    def __init__(self, timestep: timedelta):
        self.clock = self.Clock(timestep)
        self.sun = self.Sun(self.clock)
        pass
