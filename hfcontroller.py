#!/usr/bin/env python3

import argparse
import logging
from datetime import datetime, timedelta
from signal import signal, SIGINT
from suntime import Sun, SunTimeException
from timeloop import Timeloop
import time


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


clock = None
sun = None
tl = Timeloop()


class Clock:
    clock = None

    def __init__(self, timestep):
        self.time = datetime.now()
        self.clock = self

        @tl.job(interval=timedelta(seconds=timestep))
        def tick():
            self.time += timedelta(minutes=1)
            logging.info(f'time={self.time}')


class Human:
    def __init__(self):
        pass


class HFController:
    log_file = None

    class LightSensor:
        pass

    class TempSensor:
        pass

    class PresenceSensor:
        pass

    class OffButton:
        pass

    def __init__(self, has_window=True):
        pass

    def start(self):
        pass


def main(timestep, window, logfile):
    global clock
    clock = Clock(timestep)
    logging.basicConfig(filename=logfile, filemode='w', level=logging.DEBUG)
    hfcontroller = HFController(window)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timestep", help="The simulation time step for 1 minute, default is 1 second",
                        type=int, default=1)
    parser.add_argument("-w", "--window", help="The ambient light falls illuminates the controller",
                        type=bool, default=True)
    parser.add_argument("-l", "--logfile", help="Output log file name", default='nfc.log')
    args = parser.parse_args()
    main(args.timestep, args.window, args.logfile)

    tl.start(block=True)

    signal(SIGINT, handler)

    print('Running. Press CTRL-C to exit.')
    while True:
        try:
            pass
        except KeyboardInterrupt:
            print("exiting")
            exit(0)
        # Do nothing and hog CPU forever until SIGINT received.
        pass
