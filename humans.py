import datetime
import logging
import random

import world
from event import Emitter, Observer, EventData
from datetime import datetime, timedelta


class Alarm:
    def __init__(self, hours: int, minutes: int, tolerance_minutes: int, name: str, action=None):
        self.logger = logging.getLogger(__class__.__name__)
        self.triggered = False
        self.time = None
        self.alarm_time = timedelta(hours=hours, minutes=minutes)
        self.tolerance_minutes = tolerance_minutes
        self.name = name
        self.action = action
        self.rearm()

    def rearm(self):
        ct = world.env.clock.time
        midnight = ct - timedelta(hours=ct.hour, minutes=ct.minute)
        self.time = midnight + self.alarm_time + timedelta(minutes=random.uniform(0, self.tolerance_minutes))
        self.triggered = False

    def trigger(self):
        ct = world.env.clock.time
        self.logger.info(f'{ct.hour}:{ct.minute}: {self.__class__.__name__} {self.name}')
        if self.action:
            self.action()
        self.triggered = True


class Pedant(Emitter, Observer):
    ct = world.env.clock.time

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__class__.__name__)
        world.env.clock.attach(self)
        self.day = world.env.clock.time.weekday()
        self.day_flipped = False
        self.triggered_events = list()
        self.triggered_events.append(Alarm(8, 0, 20, 'Wakeup'))
        self.triggered_events.append(Alarm(9, 30, 10, 'Leave', (lambda: self.left.leave())))
        self.triggered_events.append(Alarm(22, 30, 120, 'Sleep'))
        self.triggered_events.append(Alarm(22, 30, 120, 'Sleep'))

    def update(self, event: EventData):
        super().update(event)
        for alarm in self.triggered_events:
            if self.ct >= alarm.time and not alarm.triggered:
                alarm.trigger()
        if self.day != world.env.clock.time.weekday():
            self.day_flipped = True
            self.logger.debug('-------------day switch!')
            self.day = world.env.clock.time.weekday()
        if self.day_flipped and all(alarm.triggered for alarm in self.triggered_events):
            self.day_flipped = False
            self.rearm_alarms()

    def leave(self):
        self.logger.debug(f'{self.ct.hour}:{self.ct.minute}: {self.__class__.__name__} Leave')
        pass

    def come_back(self):
        self.logger.debug(f'{self.ct.hour}:{self.ct.minute}: {self.__class__.__name__} Come back')
        pass

    def rearm_alarms(self):
        self.logger.debug('+++++++++++++rearm timers')
        for alarm in self.triggered_events:
            alarm.rearm()
        pass
