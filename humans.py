import datetime
import logging

import world
from event import Emitter, Observer


class Pedant(Emitter, Observer):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__class__.__name__)
        world.env.clock.attach(self)
        self.day = world.env.clock.time.weekday()

    def update(self, data):
        super().update(data)
        if data.weekday() != self.day:
            self.day = data.weekday()
            print(f'{self.day=}')
        pass
