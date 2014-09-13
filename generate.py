#!/usr/bin/env python
import os, datetime, sys

infile = open(sys.argv[1],"r")
lines = infile.readlines()
infile.close()

Title = lines[0].split()[1]
Class = lines[1].split()[1]

Schedule = lines[2].split()
Schedule = Schedule[1:]

DateTmp = (lines[3].split()[1]).split('.')
StartDate = datetime.date(int(DateTmp[0]), int(DateTmp[1]), int(DateTmp[2]))
if (StartDate.weekday()<>0):
    raise ValueError('New year should start from Monday!')
DateTmp = (lines[4].split()[1]).split('.')
EndDate = datetime.date(int(DateTmp[0]), int(DateTmp[1]), int(DateTmp[2]))
if (EndDate.weekday()<>0):
    raise ValueError('Year should be ended on Monday!')
if (EndDate < StartDate):
    raise ValueError('End date can not be earlier as start of the year!')


curDate = StartDate
incrDate = datetime.timedelta(days=1)
weekAB = 'a'
weekABn = curDate.isocalendar()[1]
createdCal = []
for i in range((EndDate-StartDate).days):
    if (weekABn <> curDate.isocalendar()[1]):
        if (weekAB=='a'):
            weekAB='b'
        else:
            weekAB='a'
        weekABn = curDate.isocalendar()[1]
    curWeekDay = curDate.weekday() + 1
    for sch in Schedule:
        dayD = int(sch[0])
        if (curWeekDay == dayD and weekAB in sch[1:]):
            createdCal.append(curDate)

    curDate = curDate+incrDate
    #print curDate

print createdCal
