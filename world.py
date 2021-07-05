#!/usr/bin/env python3

from datetime import datetime, timedelta, date
import logging
from suntime import Sun
import pytz

import world
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

    class Weather:
        def __init__(self):
            with open('26063.01.01.2020.31.12.2020.1.0.0.ru.utf8.00000000.csv', 'r', encoding='utf-8', errors='ignore') as f:
                data = f.readlines()[1:]
                data1 = [[col.replace('"', '') for col in line[0:2]] for line in [entry.split(';') for entry in reversed(data)]]
                self.data = dict()
                self.weather_year = datetime.strptime(data1[0][0], '%d.%m.%Y %H:%M').year
                for entry in data1:
                    timestamp = datetime.strptime(entry[0], '%d.%m.%Y %H:%M')
                    timestamp = timestamp.replace(tzinfo=World.Clock.timezone)
                    temperature = float(entry[1])
                    self.data[timestamp] = temperature
                self.min_temp = min([record for record in self.data.values()])
                self.max_temp = max([record for record in self.data.values()])

        def get_temperature(self, requested_date: datetime):
            if requested_date is None:
                requested_date = world.env.clock.time
            requested_date = requested_date.replace(year=self.weather_year)
            actual_date, temperature = min(self.data.items(), key=lambda x: abs(requested_date - x[0]))
            return temperature

    def __init__(self, timestep: timedelta):
        self.clock = self.Clock(timestep)
        self.sun = self.Sun(self.clock)
        self.weather = self.Weather()
        pass


class Bathroom:
    def __init__(self):
        self._min_unheated_temp = 16.0
        self._max_unheated_temp = 28.0
        w = world.env.weather
        medium_temp = (w.max_temp - w.min_temp) / 2 + w.min_temp
        medium_unheated = (self._max_unheated_temp - self._min_unheated_temp) / 2 + self._min_unheated_temp
        self._K = (self._max_unheated_temp - self._min_unheated_temp) / (w.max_temp - w.min_temp)
        self._shift = medium_unheated - (medium_temp * self._K)
        pass

    @property
    def temperature(self):
        outdoor_temperature_shifted = world.env.weather.get_temperature(world.env.clock.time - timedelta(hours=6))
        return round(outdoor_temperature_shifted * self._K + self._shift, 1)
