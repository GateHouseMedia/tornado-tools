import requests
from tqdm import tqdm

import datetime
import csv
import glob
import os


# https://www.spc.noaa.gov/climo/reports/190521_rpts_filtered.csv
# Tornadoes come first. So if row['Time'] = "Time", we're looking at the next type of report and need to break.
baseurlpre = "https://www.spc.noaa.gov/climo/reports/"
# baseurlpost = "_rpts_torn.csv"
baseurlpost = "_rpts_filtered.csv"
compositecsv = "composite.csv"
datadir = "data/"
startdateraw = "2019-05-01"
enddateraw = "Today"   # YYYY-mm-dd or "Today"

os.makedirs(datadir, exist_ok=True)

if enddateraw == "Today":
    enddate = datetime.datetime.now()
else:
    enddate = datetime.datetime.strptime(enddateraw, "%Y-%m-%d")
startdate = datetime.datetime.strptime(startdateraw, "%Y-%m-%d")

deltadays = (enddate - startdate).days

for i in tqdm(range(0, deltadays + 1)):
    targetdate = startdate + datetime.timedelta(days=i)
    targetfilename = datadir + targetdate.strftime("%Y-%m-%d.csv")
    targeturl = baseurlpre + targetdate.strftime("%y%m%d") + baseurlpost
    with open(targetfilename, "wb") as f:
        r = requests.get(targeturl)
        if r.status_code == 200:   # If the page is good
            f.write(r.content)
        else:
            print(f"Error retrieving file from {targeturl}")

headers = None
sourcecsvs = list(glob.glob(datadir + "*.csv"))
with open(compositecsv, "w", newline="", encoding="utf-8") as compositecsvhandle:
    writer = csv.writer(compositecsvhandle)
    for sourcecsv in sourcecsvs:
        with open(sourcecsv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            mydate = sourcecsv.replace("\\", "/").replace(datadir, "").replace(".csv", "")
            # print(mydate)
            try:
                for row in reader:
                    if not headers:
                        headers = ["mydate"]
                        headers.extend(list(row.keys()))
                        writer.writerow(headers)
                    if row['Time'] == "Time":   # if we're out of the tornado reports and into another section
                        break
                    line = [mydate]
                    line.extend(list(row.values()))                
                    writer.writerow(line)
            except:
                print(f"Something broke on {sourcecsv}")
