import datetime
import logging
import random

import world
from event import Emitter, Observer, EventData
from datetime import datetime, timedelta


class Alarm:
    def __init__(self, hours: int, minutes: int, tolerance_minutes: int, name: str):
        self.triggered = False
        self.time = None
        self.alarm_time = timedelta(hours=hours, minutes=minutes)
        self.tolerance_minutes = tolerance_minutes
        self.name = name
        self.rearm()

    def rearm(self):
        ct = world.env.clock.time
        midnight = ct - timedelta(hours=ct.hour, minutes=ct.minute)
        self.time = midnight + self.alarm_time + timedelta(minutes=random.uniform(0, self.tolerance_minutes))
        self.triggered = False


class Pedant(Emitter, Observer):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__class__.__name__)
        world.env.clock.attach(self)
        self.day = world.env.clock.time.weekday()
        self.triggered_events = list()
        self.triggered_events.append(Alarm(8, 0, 20, 'Wakeup'))

    def update(self, event: EventData):
        super().update(event)
        ct = world.env.clock.time
        for alarm in self.triggered_events:
            if ct >= alarm.time and not alarm.triggered:
                self.logger.info(f'{ct.hour}:{ct.minute}: {self.__class__.__name__} {alarm.name}')
                alarm.triggered = True
        if event.data.weekday() != self.day:
            self.day = event.data.weekday()
            self.rearm_alarms()

    def rearm_alarms(self):
        for alarm in self.triggered_events:
            alarm.rearm()
        pass
