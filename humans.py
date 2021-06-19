import datetime
import logging
from abc import ABC, abstractmethod
from random import uniform

import world
from event import Emitter, Observer, EventData
from datetime import datetime, timedelta, time


class Pedant(Emitter, Observer):
    class AlarmCondition(ABC):
        @abstractmethod
        def check(self):
            raise NotImplementedError
            pass

    class PeriodicCondition(AlarmCondition):
        def __init__(self, minutes: int):
            self.minutes = minutes

        def check(self):
            s = (1 / (timedelta(minutes=self.minutes).seconds // 60))
            p = uniform(0, 1) < s
            return p

    class ExpireCondition(AlarmCondition):
        def __init__(self, timeout: int, tolerance: int = 0):
            self.timeout = timeout
            self.tolerance = tolerance
            self._rearm()

        def check(self):
            if world.env.clock.time >= self.deadline_time:
                self._rearm()
                return True
            return False

        def _rearm(self):
            alarm_time = world.env.clock.time + timedelta(minutes=self.timeout)
            self.deadline_time = uniform(alarm_time, alarm_time + timedelta(minutes=self.tolerance))

    class TimeCondition(AlarmCondition):
        def __init__(self, hours: int, minutes: int, tolerance: int):
            self.time = time(hour=hours, minute=minutes)
            self.tolerance = timedelta(minutes=tolerance)
            self.alarm_time = datetime.combine(world.env.clock.time, self.time, tzinfo=world.World.Clock.timezone)
            self.deadline_time = uniform(self.alarm_time, self.alarm_time + self.tolerance)

        def check(self):
            if world.env.clock.time >= self.deadline_time:
                self._rearm()
                return True
            return False

        def _rearm(self):
            alarm_date = world.env.clock.time.date()
            if self.deadline_time.date() == self.alarm_time.date():
                alarm_date += timedelta(days=1)
            self.alarm_time = datetime.combine(alarm_date, self.time, tzinfo=world.World.Clock.timezone)
            self.deadline_time = uniform(self.alarm_time, self.alarm_time + self.tolerance)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__class__.__name__)
        world.env.clock.attach(self)
        self.day = world.env.clock.time.weekday()
        self.states = {
            "sleep": [{
                "to": "idle",
                "condition": Pedant.TimeCondition(8, 0, 20),
            }, {
                "to": "nightpee",
                "condition": Pedant.PeriodicCondition(8 * 60)
            }],
            "idle": [{
                "to": "sleep",
                "condition": Pedant.TimeCondition(23, 00, 120),
            }, {
                "to": "biobreak",
                "condition": Pedant.PeriodicCondition(120)
            }],
            "nightpee": [{
                "to": "sleep",
                "condition": Pedant.ExpireCondition(5)
            }],
            "biobreak": [{
                "to": "idle",
                "condition": Pedant.ExpireCondition(3, 15)
            }]
        }

        self.state = self.states['sleep']

    def update(self, event: EventData):
        super().update(event)

        for transition in self.state:
            if transition['condition'].check():
                self.logger.debug(f'{world.env.clock.time}: {self.__class__.__name__} Going to state {transition["to"]}')
                self.state = self.states[transition['to']]

        if self.day != world.env.clock.time.weekday():
            self.logger.debug('-------------day switch!')
            self.day = world.env.clock.time.weekday()

    def leave(self):
        self.logger.debug(f'{world.env.clock.time}: {self.__class__.__name__} Leave')
        pass

    def come_back(self):
        self.logger.debug(f'{world.env.clock.time}: {self.__class__.__name__} Come back')
        pass

    def rearm_alarms(self):
        self.logger.debug('+++++++++++++rearm timers')
