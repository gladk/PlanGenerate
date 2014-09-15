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


#=====================
def DayOfWeek(d):
    if (d==1):
        return "Mo"
    elif (d==2):
        return "Di"
    elif (d==3):
        return "Mi"
    elif (d==4):
        return "Do"
    elif (d==5):
        return "Fr"
    else:
        return "None"
#=====================

#=====================
#Load Holidays
FreeDaysDate = []
FreeDaysName = []
HolidayName = ""
for i in range(7, len(lines)):
    if (i+1 < len(lines) and ((lines[i+1])[10:]).strip()==''):  #Holidays
        DateTmp = (lines[i].split()[0]).split('.')
        StartHol = datetime.date(int(DateTmp[0]), int(DateTmp[1]), int(DateTmp[2]))
        
        DateTmp = (lines[i+1].split()[0]).split('.')
        EndHol = datetime.date(int(DateTmp[0]), int(DateTmp[1]), int(DateTmp[2]))
        HolidayName = (lines[i])[10:].strip()
        if (EndHol < StartHol):
            raise ValueError(('End date of the holiday %s can not be earlier as start of the year!')%(HolidayName))
        
        curDateH = StartHol
        incrDate = datetime.timedelta(days=1)
        while (curDateH <> EndHol):
            curDateH += incrDate
            FreeDaysDate.append(curDateH)
            FreeDaysName.append(HolidayName)
    elif ((lines[i])[10:].strip()==''):
        continue
    else:
        DateTmp = (lines[i].split()[0]).split('.')
        DateHol = datetime.date(int(DateTmp[0]), int(DateTmp[1]), int(DateTmp[2]))
        HolidayName = (lines[i])[10:].strip()
        FreeDaysDate.append(DateHol)
        FreeDaysName.append(HolidayName)
    #print "%s is added" %(HolidayName)

#=====================

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

#=====================

createdCalNames = [""]*len(createdCal)
for i in range(len(createdCal)):
    if createdCal[i] in FreeDaysDate:
        FerienN = "";
        for z in range(len(FreeDaysDate)):
            if createdCal[i] == FreeDaysDate[z]:
                if (FerienN==""):
                    FerienN=FreeDaysName[z]
                else:
                    FerienN+="; " + FreeDaysName[z]
        createdCalNames[i] = FerienN

"""
for i in range(len(createdCal)):
    print "%s - %s" % (createdCal[i], createdCalNames[i])
"""
outputGenCalendar = ""
for i in range(6):
    outputGenCalendar+=lines[i]

outputGenCalendar+="N;\tWeek;\tWeekAB;\tDate;\tFreeDay;\tDoW;\tHrs;\tTopic\n" 

WeekN = 1
WeekAB = 'a'
Hrs = 0
for i in range(len(createdCal)):
    if (i<>0 and createdCal[i].isocalendar()[1] <> createdCal[i-1].isocalendar()[1]):
        WeekN+=1
        if (WeekAB=='a'):
            WeekAB='b'
        else:
            WeekAB='a'
    FreeDay=""
    if createdCalNames[i]<>"":
        FreeDay="F"
    else:
        FreeDay="-"
        Hrs+=1
    outputGenCalendar+="%d;\t%d;\t%s;\t%s;\t%s;\t%s;\t%d;\t%s;\t;\n"%(i+1,
        WeekN, WeekAB, createdCal[i], FreeDay, DayOfWeek(createdCal[i].isocalendar()[2]),
        Hrs, createdCalNames[i])

file(sys.argv[1]+'.gencalendar','w').write(outputGenCalendar)
