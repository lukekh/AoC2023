"""Get puzzle inputs"""
import time
import datetime
import sys
import requests
import credentials

class ScrapeError(Exception):
    """Error class for scraping error"""


def scrape(n):
    """
    Scrape AoC website for inputs
    """
    s = 'Day' + str(n).zfill(2)

    uri = f'https://adventofcode.com/2022/day/{n}/input'

    d = datetime.datetime(2022, 12, n, 15, 30, 0)
    delta = time.mktime(d.timetuple()) - time.time()

    if delta < 61:
        print('*'*23)
        if delta > 0:
            print(f'Waiting {delta:.0f}s for puzzle drop')
            time.sleep(delta + 0.01)

        print('Getting inputs')
        with requests.Session() as r:
            response = r.get(uri, cookies=credentials.SESSION_COOKIE, timeout=5).text

        print(f'Writing to {s}/{s}.in')
        with open(f"{s}/{s}.in", 'w', encoding="utf8") as f:
            f.write(response)

        print("Happy puzzling!\n"+ '*'*23)
    else:
        raise ScrapeError("You are running this too early.")

if __name__ == "__main__":
    # If an argument is passed to script, run for that day else do next day from max
    if len(sys.argv) > 1:
        date = int(sys.argv[1])
        scrape(date)
    else:
        print("Specify day when running as main.\nE.g. py scrape.py <day>")
