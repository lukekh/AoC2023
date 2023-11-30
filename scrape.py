"""Get puzzle inputs"""
import datetime
import sys
import time
import requests
import credentials

class RequestError(Exception):
    """Problem with request"""

class EarlyError(Exception):
    """You're too keen, apparently"""


def scrape(n):
    """
    Scrape AoC website for inputs
    """
    uri = f'https://adventofcode.com/2023/day/{n}/input'

    d = datetime.datetime(2023, 12, n, 15, 30, 0)
    delta = time.mktime(d.timetuple()) - time.time()

    if delta < 61:
        print('*'*23)
        if delta > 0:
            print(f'Waiting {delta:.0f}s for puzzle drop')
            time.sleep(delta + 0.01)

        print('Getting inputs')
        with requests.Session() as r:
            response = r.get(uri, cookies=credentials.credentials, timeout=5)

        if response.status_code == 200:
            return response.text
        else:
            raise RequestError(f"Got status={response.status_code}, reason={response.reason}")
    else:
        raise EarlyError("You are running this too early.")

if __name__ == "__main__":
    # If an argument is passed to script, run for that day else do next day from max
    if len(sys.argv) > 1:
        date = int(sys.argv[1])
        scrape(date)
    else:
        print("Specify day when running as main.\nE.g. py scrape.py <day>")
