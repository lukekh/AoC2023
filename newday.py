"""
Create a new folder for the current day
"""
import os
import sys
import shutil
import re
from scrape import scrape, ScrapeError


def main(day=None):
    """
    Create new folder for AoC puzzle and try to scrape for puzzle inputs
    """
    # Static vars
    template = 'Template/'
    pattern = r'Day(\d{2})'

    if day is None:
        # Get next day from folder structure
        day_folder_numbers = [int(re.search(pattern, i)[1]) for i in os.listdir() if re.search(pattern, i)]
        n = max(day_folder_numbers)+1 if day_folder_numbers else 1
    elif os.path.isdir('Day' + str(day).zfill(2)):
        raise FileExistsError(f"Folder {'Day' + str(day).zfill(2)} already exists")
    else:
        n = day

    s = 'Day' + str(n).zfill(2)

    # Copy Template folder
    shutil.copytree(template, s)

    folder = s + '/'

    with open(folder +'DayXX.py', 'r+', encoding="utf8") as f:
        t = f.read()
        f.seek(0)
        t = t.replace('DayXX', s).replace('XX', f'{n}')
        f.write(t)
        f.truncate()

    for file in os.listdir(folder):
        os.rename(folder+file, folder+file.replace('DayXX', s))

    try:
        scrape(n)
    except ScrapeError:
        print("Try scraping closer to puzzle release.")

if __name__ == "__main__":
    # If an argument is passed to script, run for that day else do next day from max
    if len(sys.argv) > 1:
        d = int(sys.argv[1])
    else:
        d = None

    main(day=d)
