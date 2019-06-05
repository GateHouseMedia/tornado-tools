import requests
from tqdm import tqdm

import datetime
import csv
import glob
from time import sleep
import os

naptime = 0.2   # How many seconds to sleep between downloads?
MaxDaysOld = 30   # Re-download every file newer than XX days old

# https://www.spc.noaa.gov/climo/reports/190521_rpts_filtered.csv
# Tornadoes come first in the file. So if row['Time'] = "Time", we're looking at the next type of report and need to break.
# We're not attempting to parse out hail and other report types.
baseurlpre = "https://www.spc.noaa.gov/climo/reports/"
# baseurlpost = "_rpts_torn.csv"
baseurlpost = "_rpts_filtered.csv"
compositecsv = "DailyComposite-"
filepre = "Daily"
datadir = "data/"
startdateraw = "2012-01-01"
enddateraw = "Today"   # YYYY-mm-dd or "Today"

os.makedirs(datadir, exist_ok=True)

timenow  = datetime.datetime.now()   # Don't alter.
timestampnow = datetime.datetime.strftime(timenow, "%Y-%m-%d_%I%M%p")

if enddateraw == "Today":
    enddate = datetime.datetime.now()
else:
    enddate = datetime.datetime.strptime(enddateraw, "%Y-%m-%d")
startdate = datetime.datetime.strptime(startdateraw, "%Y-%m-%d")

deltadays = (enddate - startdate).days

for i in tqdm(range(0, deltadays + 1)):
    targetdate = startdate + datetime.timedelta(days=i)
    targetfilename = datadir + filepre + targetdate.strftime("%Y-%m-%d.csv")
    targeturl = baseurlpre + targetdate.strftime("%y%m%d") + baseurlpost
    WantFile = True
    if os.path.exists(targetfilename):
        filedatestamp = datetime.datetime.fromtimestamp(os.path.getmtime(targetfilename))
        if ((filedatestamp - targetdate).days + 2) > MaxDaysOld:
            WantFile = False
    if WantFile:
        r = requests.get(targeturl)
        if r.status_code == 200:   # If the page is good
            with open(targetfilename, "wb") as f:
                f.write(r.content)
        else:
            print(f"Error retrieving file from {targeturl}")
        sleep(naptime)

headers = None
sourcecsvs = list(glob.glob(datadir + filepre + "*.csv"))
with open(f"{compositecsv}{timestampnow}.csv", "w", newline="", encoding="utf-8") as compositecsvhandle:
    writer = csv.writer(compositecsvhandle)
    for sourcecsv in sourcecsvs:
        with open(sourcecsv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            mydate = sourcecsv.replace("\\", "/").replace(datadir, "").replace(".csv", "").replace(filepre, "")
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
