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

        @abstractmethod
        def rearm(self):
            raise NotImplementedError
            pass

    class PeriodicCondition(AlarmCondition):
        def __init__(self, minutes: int):
            self.minutes = minutes

        def check(self):
            s = (1 / (timedelta(minutes=self.minutes).seconds // 60))
            p = uniform(0, 1) < s
            return p

        def rearm(self):
            pass

    class ExpireCondition(AlarmCondition):
        def __init__(self, timeout: int, tolerance: int = 0):
            self.timeout = timeout
            self.tolerance = tolerance

        def check(self):
            if world.env.clock.time >= self.deadline_time:
                return True
            return False

        def rearm(self):
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
                self.rearm()
                return True
            return False

        def rearm(self):
            if self.deadline_time > world.env.clock.time:
                return

            self.alarm_time = datetime.combine(world.env.clock.time.date(), self.time, tzinfo=world.World.Clock.timezone)
            self.deadline_time = uniform(self.alarm_time, self.alarm_time + self.tolerance)
            # did we set alarm in the past? move one day forward
            if self.deadline_time <= world.env.clock.time:
                self.alarm_time += timedelta(days=1)
                self.deadline_time += timedelta(days=1)
            # did we set alarm too far in future? move one day back
            elif self.deadline_time - timedelta(days=1) > world.env.clock.time:
                self.alarm_time -= timedelta(days=1)
                self.deadline_time -= timedelta(days=1)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__class__.__name__)
        world.env.clock.attach(self)
        self.day = world.env.clock.time.weekday()
        self.states = {
            "workday": {
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
                    }, {
                    "to": "shower",
                    "condition": Pedant.TimeCondition(8, 20, 10)
                    }, {
                    "to": "leave",
                    "condition": Pedant.TimeCondition(9, 25, 30)
                }],
                "nightpee": [{
                    "to": "sleep",
                    "condition": Pedant.ExpireCondition(5)
                }],
                "biobreak": [{
                    "to": "idle",
                    "condition": Pedant.ExpireCondition(3, 15)
                }],
                "shower": [{
                    "to": "idle",
                    "condition": Pedant.ExpireCondition(15, 10)
                }],
                "leave": [{
                    "to": "idle",
                    "condition": Pedant.TimeCondition(19, 0, 180)
                }]
            },
            "weekend": {
                "sleep": [{
                    "to": "idle",
                    "condition": Pedant.TimeCondition(9, 0, 120),
                    }, {
                    "to": "nightpee",
                    "condition": Pedant.PeriodicCondition(8 * 60)
                }],
                "idle": [{
                    "to": "sleep",
                    "condition": Pedant.TimeCondition(22, 0, 240),
                    }, {
                    "to": "biobreak",
                    "condition": Pedant.PeriodicCondition(120)
                    }, {
                    "to": "shower",
                    "condition": Pedant.TimeCondition(9, 30, 120)
                    }, {
                    "to": "leave",
                    "condition": Pedant.TimeCondition(8, 22, 12*60)
                }],
                "nightpee": [{
                    "to": "sleep",
                    "condition": Pedant.ExpireCondition(5)
                }],
                "biobreak": [{
                    "to": "idle",
                    "condition": Pedant.ExpireCondition(3, 15)
                }],
                "shower": [{
                    "to": "idle",
                    "condition": Pedant.ExpireCondition(15, 10)
                }],
                "leave": [{
                    "to": "idle",
                    "condition": Pedant.TimeCondition(19, 0, 180)
                }]
            }
        }

        self.state = ['workday', 'sleep']
        self.transit()

    def transit(self):
        work_state = self._get_work_state()
        if work_state != self.state[0]:
            self.state[0] = work_state
            self.logger.info(f'{world.env.clock.time}: {self.state}')
            for alarm in self.states[self.state[0]][self.state[1]]:
                alarm['condition'].rearm()

        for transition in self.states[work_state][self.state[1]]:
            if transition['condition'].check():
                self.state[1] = transition['to']
                self.logger.info(f'{world.env.clock.time}: {self.state}')
                for alarm in self.states[self.state[0]][self.state[1]]:
                    alarm['condition'].rearm()

    def update(self, event: EventData):
        super().update(event)

        self.transit()

        if self.day != world.env.clock.time.weekday():
            self.logger.info('-------------day switch!')
            self.day = world.env.clock.time.weekday()

    def _get_work_state(self):
        if self.day < 5:
            return 'workday'
        return 'weekend'

    def leave(self):
        self.logger.debug(f'{world.env.clock.time}: {self.__class__.__name__} Leave')
        pass

    def come_back(self):
        self.logger.debug(f'{world.env.clock.time}: {self.__class__.__name__} Come back')
        pass
