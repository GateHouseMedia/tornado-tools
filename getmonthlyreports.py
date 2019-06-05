import requests
from pyquery import PyQuery as pq
from tqdm import tqdm

import glob
import csv
import os
from collections import OrderedDict
from time import sleep
import datetime

naptime = 0.2
MaxDaysOld = 80   # Download all monthly summaries that are less than XX days old
baseurlpre = "https://www.spc.noaa.gov/climo/online/monthly/"
baseurlpost = "_summary.html"
datadir = "data/"
headers = ["Day", "Total", "Torn", "Hail", "Wind"]
reportname = "MonthlyComposite.csv"

timenow = datetime.datetime.now()
yearnow = timenow.year % 100
monthnow = timenow.month

stufftopull = []
for myyear in range(0, yearnow + 1):    # Reports seem to begin in 2000
    for mymonth in range(0, 12 + 1):   # End every year in December
        if myyear == yearnow and mymonth > monthnow:
            break   # Quit trying to pull from the future
        stufftopull.append(f"{myyear:02d}{mymonth:02d}")

for yearmo in tqdm(stufftopull):
    filename = f"{datadir}Monthly{yearmo}.html"
    WantFile = True
    if os.path.exists(filename):
        filedatestamp = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        targetdate = datetime.datetime.strptime(yearmo + "01", "%y%m%d")
        if ((filedatestamp - targetdate).days + 2) > MaxDaysOld:
            WantFile = False
    if WantFile:
        remoteurl = f"{baseurlpre}{yearmo}{baseurlpost}"
        r = requests.get(remoteurl)
        if r.status_code == 200:   # if we got a good file
            with open(filename, "wb") as f:
                f.write(r.content)
            sleep(naptime)

masterlist = []
monthlyreports = list(glob.glob(datadir + "Monthly*.html"))
for monthlyreport in monthlyreports:
    with open(monthlyreport, "r") as f:
        html = f.read()
    table = pq(html)("table")[8]
    for row in pq(table)("tr")[1:-1]:    # Skip header and total row
        line = OrderedDict()
        datetemp = pq(pq(row)("td")[0]).text().strip().split("/")
        line['Date'] = f"{datetemp[2]}-{datetemp[0]}-{datetemp[1]}"
        for i, cell in enumerate(pq(row)("td")[1:]):
            line[headers[i + 1]] = int(pq(cell).text().strip())
        masterlist.append(line)

with open(reportname, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for row in masterlist:
        writer.writerow(list(row.values()))
