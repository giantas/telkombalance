#! /usr/bin/env python3

import schedule
import time

from balance import query

if __name__ == "__main__":
    schedule.every(30).seconds.do(query)

    while True:
        schedule.run_pending()
        time.sleep(1)
