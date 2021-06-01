#!/usr/bin/env python3

import argparse
from abc import ABC, abstractmethod
import logging
from datetime import datetime, timedelta
from signal import signal, SIGINT
from suntime import Sun, SunTimeException
from timeloop import Timeloop
import time
from typing import List


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


clock = None
sun = None
tl = Timeloop()


class Ticker(ABC):
    @abstractmethod
    def tick(self, stime: datetime):
        pass


class Clock(ABC):
    _clock = None
    _tickers: List[Ticker] = []

    def attach(self, ticker: Ticker) -> None:
        self._tickers.append(ticker)

    def detach(self, ticker: Ticker) -> None:
        self._tickers.remove(ticker)

    def notify(self) -> None:
        for ticker in self._tickers:
            ticker.tick(self.time)

    def __init__(self, timestep):
        self.time = datetime.now()
        self._clock = self

        @tl.job(interval=timedelta(seconds=timestep))
        def tick():
            self.time += timedelta(minutes=1)
            logging.info(f'time={self.time}')
            self.notify()


class Human:
    def __init__(self):
        pass


class HFController:
    log_file = None
    light_sensor = None

    class LightSensor(Ticker):

        def __init__(self):
            clock.attach(self)

        def on_light(self):
            pass

        def on_dark(self):
            pass

        def tick(self, stime: datetime) -> None:
            pass

    class TempSensor:
        pass

    class PresenceSensor:

        def on_presence(self):
            pass

    class TeachButton:

        def on_press(self):
            pass

    def __init__(self, has_window=True):
        light_sensor = self.LightSensor()
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
