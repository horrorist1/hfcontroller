import datetime
import logging

import world
from event import Emitter, Observer


class Alarm:
    def __init__(self, time):
        datetime.timedelta.
        self.time = datetime.datetime.strptime(time, '%H:%M:%S').time()
        self.triggered = False


class Pedant(Emitter, Observer):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__class__.__name__)
        world.env.clock.attach(self)
        self.schedule = Alarm('08:11:10')

    def update(self, data):
        super().update(data)
        if data >= datetime.datetime.today() + self.schedule.time and not self.schedule.triggered:
            self.logger.info(f' light is {data}')
            self.schedule.triggered = True
        pass
