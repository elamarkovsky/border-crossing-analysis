# Import libraries and define variables

import csv
from pprint import pprint
from datetime import datetime
from operator import itemgetter
import os.path
total = 0

# Import data in csv format
#path = r"C:\Users\elama\PycharmProjects\BorderCrossings\input\Border_Crossing_Entry_Data.csv"
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, "..","input", "Border_Crossing_Entry_Data.csv")

with open(path, "r") as data:
    reader = csv.DictReader(data)
    # Create emtpy dictionary to store data
    crossings = {}
    crossings2 = {}
    # Read and process the input file
    for line in reader:
        raw_border, raw_date, raw_measure, raw_value = line["Border"], line["Date"], line["Measure"], line["Value"]
        border = raw_border
        measure = raw_measure
        events = int(raw_value)
        cross_date = datetime.strptime(raw_date, "%m/%d/%Y %I:%M:%S %p")
        #print(cross_date.month)
        try:
            events = int(raw_value)
            cross_date = datetime.strptime(raw_date, "%m/%d/%Y %I:%M:%S %p")
        except ValueError:
            continue

        # Create a nested dictionary with structure: date -> measure, border - > events
        # Create dates dictionary
        if cross_date not in crossings:
            crossings[cross_date] = {}
        crossings_for_date = crossings[cross_date]
        # Create measures-borders dictionary inside dates dictionary and sum up events with the same measure and border
        m_b = (measure, border)
        if m_b not in crossings_for_date:
            crossings_for_date[m_b] = events
        else:
            crossings_for_date[m_b] = crossings_for_date[m_b] + events

# Sort entries in descending order and print out
dates = list(crossings.keys())
dates.sort()
count = 0
running_sum = 0
for index, date in enumerate(dates):
    for measure, border in crossings[date]:
        new_value = None
        for back in reversed(dates[:index]):
            if (measure,border) not in crossings[back]:
                continue
            prev_value = crossings[back][(measure,border)]
            new_value = (crossings[date][(measure,border)], prev_value[1]+1, prev_value[2]+prev_value[0])
            crossings[date][(measure, border)] = new_value
            break
        if new_value is None:
            crossings[date][(measure, border)] = (crossings[date][(measure,border)], 0, 0)

dates = list(crossings.keys())
dates.sort(reverse=True)

path_out = os.path.join(dirname, "..","output", "report.csv")
with open(path_out, mode='w', newline='') as report_file:
    report_writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    report_writer.writerow(["Border", "Date", "Measure", "Value", "Average"])
    for date in dates:
        measures_borders = list(crossings[date].items())
        measures_borders.sort(key=itemgetter(1), reverse=True)
        for m_b in measures_borders:
            border = m_b[0][1]
            measure = m_b[0][0]
            value=m_b[1][0]
            date_time = date.strftime("%m/%d/%Y %I:%M:%S %p")
            if m_b[1][1] == 0:
                average = 0
            else:
                average=round(m_b[1][2]/m_b[1][1])
            report_writer.writerow([border, date_time, measure,value,average])