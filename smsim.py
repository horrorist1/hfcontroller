#!/usr/bin/env python3

import argparse
import logging
import sys
from datetime import timedelta

import humans
from hfcontroller import HFController
import time
import world

controller = None


def main(timestep, has_window, logfile, debug):
    logging_level = logging.INFO
    if debug:
        logging_level = logging.DEBUG
    if logfile is not None:
        logging.basicConfig(stream=sys.stdout, level=logging_level)
    else:
        logging.basicConfig(filename=logfile, filemode='w', level=logging_level)
    world.env = world.World(timestep=timestep)
    world.bathroom = world.Bathroom()
    global controller
    human = humans.Pedant()
    controller = HFController(human, has_window)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timestep", help="The simulation time step for 1 minute, default is 1000 microseconds",
                        type=int, default=1000)
    parser.add_argument("-w", "--window", help="The ambient light falls illuminates the controller",
                        action='store_true', dest='window')
    parser.add_argument("-l", "--logfile", help="Output log file name", default=sys.stdout)
    parser.add_argument("-d", "--debug", help="Debug output enabled",
                        action='store_true', dest='debug')
    args = parser.parse_args()
    main(timedelta(microseconds=args.timestep), args.window, args.logfile, args.debug)

    print('Running. Press CTRL-C to exit.')
    while True:
        try:
            world.env.clock.tick()
        except KeyboardInterrupt:
            break
