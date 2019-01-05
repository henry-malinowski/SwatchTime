#!/usr/bin/env -S python3 -u
import argparse
import datetime
import math
import os
import signal
import time
import types
from typing import List


class SwatchTime:

    @staticmethod
    def get_beat(now: datetime.datetime = datetime.datetime.utcnow() + datetime.timedelta(hours = 1)) -> int:
        """
        Returns the current time as an integer representing the numbers of .beats into the day.
        :param now: A datetime object of some time.
        :rtype: int
        :return: int The .beat of the current moments in `now`'s day.
        """
        return math.floor(
            now.hour * 41.666 +
            now.minute * 0.6944 +
            now.second * 0.011574
        ) % 1000

    @staticmethod
    def print_swatch(now: datetime.datetime, time_format: str):
        """
        Prints the swatch time as specified in time_format
        :param now: The current time at UT1
        :param time_format: The time format string.
        """
        now += datetime.timedelta(hours=1)
        beat = SwatchTime.get_beat(now)
        time_format = time_format.replace('{Beat}', '{0:03d}'.format(beat))
        time_format = time_format.replace('{beat}', str(beat))
        print(now.strftime(time_format))


class PrintCycle:

    def __init__(self, argv: argparse.Namespace):
        self.use_swatch = True
        self.args = argv

    def loop(self):
        """
        Infinite loop that prints and waits.
        """
        while True:
            PrintCycle.print_datetime(self)
            time.sleep(self.args.delay)

    def print_datetime(self):
        """
        Prints a date/time code based on the state of self.use_swatch
        """
        if self.use_swatch:
            SwatchTime.print_swatch(datetime.datetime.utcnow(), self.args.format)
        else:
            PrintCycle.print_alt_format(self)

    def print_alt_format(self):
        """
        Prints a standard date/time code based on the utc argument. Else use local time.
        """
        if not self.args.utc:
            now = datetime.datetime.now()
        else:
            now = datetime.datetime.utcnow()

        print(now.strftime(self.args.alt_format))

    def handler_toggle_format(self, signum: int, frame: types.FrameType):
        """
        Only toggle if alt_format is set. If it is set, one-shot the print function to ensure the user doesn't wait a
        second for the printout to update.
        """
        if self.args.alt_format is not None:
            self.use_swatch = not self.use_swatch
            self.print_datetime()


def handler_print_pid(signum: int, frame: types.FrameType):
    """
    Prints the PID of the script to stdout
    """
    print('PID: {0}'.format(os.getpid()))
    time.sleep(4)


def handler_exit(signum: int, frame: types.FrameType):
    exit(0)


def get_args(argv: List[str] = None) -> argparse.Namespace:
    # ArgumentDefaultsHelpFormatter can show the defaults for us
    parser = argparse.ArgumentParser(
        description='Give date and time as Swatch Internet Time.',
    )
    parser.add_argument('-v', '--verbose',
                        help='Shows the PID for a few seconds before starting. Default: False',
                        action='store_true')
    parser.add_argument('-t', '--tail',
                        help='Enables tail output mode. Default: False',
                        action='store_true')
    parser.add_argument('-d', '--delay',
                        help='Set the delay between refreshes in tail mode; only applies if tail mode is set.',
                        type=float,
                        default=1.0)
    # TODO fix line wrapping in format
    parser.add_argument('-f', '--format',
                        help='A strftime compliant string to format the date portion of the Swatch time. '
                             '{Beat} displays the number of beats with left-padding zeros. '
                             '{beat} displays the number of beats without padding zeros. ',
                        type=str,
                        default='d%d.%m.%y@{Beat}'
                        )
    parser.add_argument('--alt-format',
                        help='Format to switch to after receiving a USR1 signal; only applies if tail output is set. '
                             'Default: None',
                        type=str)
    parser.add_argument('-u', '--utc', '--universal',
                        help='Display standard time as UTC (Coordinated Universal Time). Default: False.',
                        action='store_true')
    return parser.parse_args(argv)


def main():
    args = get_args()

    # this is for one-shotting the program to get Swatch Internet time
    if args.tail is False:
        SwatchTime.print_swatch(datetime.datetime.utcnow(), args.format)
        exit(0)

    time_cycle = PrintCycle(args)

    # Set USR* signals on Unix based systems and SIGINT as an alternative on Windows based systems
    if os.name == 'nt':
        signal.signal(signal.SIGINT, time_cycle.handler_toggle_format)
    else:
        signal.signal(signal.SIGUSR1, time_cycle.handler_toggle_format)
        signal.signal(signal.SIGUSR2, handler_print_pid)

    # print the programs PID if it is requested
    if args.verbose:
        print('PID: {0}'.format(os.getpid()))

    time_cycle.loop()


if __name__ == '__main__':
    main()
