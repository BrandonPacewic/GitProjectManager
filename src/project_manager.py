# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import argparse
import os

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    ENDCOLOR = '\033[0m'


class Timer:
    def __init__(self) -> None:
        self.tics = [time.perf_counter()]

    def tic(self) -> None:
        self.tics.append(time.perf_counter())

    def elapsed(self) -> str:
        try:
            return str('{}:.3f'.format(self.tics[-1] - self.tics[0])))
        except IndexError:
            return '0.000'


def main() -> None:
    pass



if __name__ == '__main__':
    main()