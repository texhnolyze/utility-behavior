#!/usr/bin/env python3

import signal
import sys
import time
from .action_decider import ActionDecider

decider = ActionDecider()


def main():
    try:
        while True:
            start_time = time.time()
            decider.decide()
            end_time = time.time()
            print(f"Runtime: {end_time - start_time}")
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
