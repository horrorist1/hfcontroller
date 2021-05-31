#!/usr/bin/env python3

import argparse
from datetime import datetime
import threading
import timeloop


class Clock:
    def __init__(self, tick_for_minute):
        self.time = datetime.now()
        self.tick = tick_for_minute

    def start(self):
        threading.Timer(self.tick, self.do_tick).start()

    def do_tick(self):
        print("tick")


class HFController:
    log_file = None

    class LightSensor:
        def __init__(self):
            pass

    def __init__(self, log_file, clock):
        self.log_file = log_file
        self.light_sensor = self.LightSensor()

    def start(self):
        pass


def main(tick):
    global_time = Clock(tick)
    with open('hfc.log', 'w') as log:
        hfcontroller = HFController(log, global_time)
        hfcontroller.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tick", help="The tick time for the system in minutes", type=int, default=1)
    args = parser.parse_args()
    main(args.tick)
