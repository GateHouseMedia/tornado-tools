# Tornado tools

These tools are being released by GateHouse Media after they were used internally to look at a large series of tornadoes that struck the United States in May 2019.

Three scrapers were built. The names are not meant to confuse.

All files were built and tested with Python 3.7. Required software for most of the scrapers can be installed with *pip install -r requirements.txt* ... but you might need to install Jupyter separately if you want to mess with the old storm events data.

 - **gettornadoes.py** -- This is probably what you want. This will grab all preliminary tornado reports, filtered for duplicates, that were issued since January 2012. Each row is one tornado. It comes with some data; it will fetch and update what is needed, then will build a filename like DailyComposite-2019-06-05_0257PM.csv, which shows June 5, 2019, at 2:57 p.m. Sample data: https://www.spc.noaa.gov/climo/reports/190602_rpts_filtered.csv  NOTE: These daily reports CSVs will include hail and high-wind reports, but only tornadoes are processed into the output. Pull requests are welcomed.
 - **getmonthlyreports.py** -- This collects tallies of reported storms since January 2000 -- no actual tornado-level data is available. The resulting file MonthlyComposite will show totals by day of reported tornadoes, hail and high winds. Sample report: https://www.spc.noaa.gov/climo/online/monthly/1905_summary.html   This is pulling from that "Daily tabulation" area.
- **get old storm events.ipynb** -- Jupyter Notebook file that will pull reported storm information since 1950. The more recent stuff will be somewhat out of date. We've found a number of reported tornadoes from the other data sets that do not appear in this dataset. Caution is urged. This is pulling files from https://www1.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/ . This will download several hundred megabytes of compressed data, and turn it into a CSV of more than 1 gigabyte. It may take a while.


