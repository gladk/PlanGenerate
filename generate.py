#!/usr/bin/env python
import os, datetime, sys, subprocess

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
curLineNumb = 0
for i in range(7, len(lines)):
    curLineNumb = i
    if (lines[i].strip()==""):
        break;
    if (i+1 < len(lines) and ((lines[i+1])[10:]).strip()=='' and ((lines[i+1])).strip()<>''):  #Holidays
        DateTmp = (lines[i].split()[0]).split('.')
        StartHol = datetime.date(int(DateTmp[0]), int(DateTmp[1]), int(DateTmp[2]))
        
        DateTmp = (lines[i+1].split()[0]).split('.')
        EndHol = datetime.date(int(DateTmp[0]), int(DateTmp[1]), int(DateTmp[2]))
        HolidayName = (lines[i])[10:].strip()
        if (EndHol < StartHol):
            raise ValueError(('End date of the holiday %s can not be earlier as start of the year!')%(HolidayName))
        
        curDateH = StartHol
        incrDate = datetime.timedelta(days=1)
        while (curDateH <= EndHol):
            FreeDaysDate.append(curDateH)
            FreeDaysName.append(HolidayName)
            curDateH += incrDate
            
    elif ((lines[i])[10:].strip()==''):
        continue
    else:
        DateTmp = (lines[i].split()[0]).split('.')
        DateHol = datetime.date(int(DateTmp[0]), int(DateTmp[1]), int(DateTmp[2]))
        HolidayName = (lines[i])[10:].strip()
        FreeDaysDate.append(DateHol)
        FreeDaysName.append(HolidayName)
curLineNumb+=1
#=====================
# Load topics
topics = []
topicsCommon = []
for i in range(curLineNumb,len(lines)):
    lineStrip = lines[i].strip()
    if (len(lineStrip.split('|'))>1):
        topics.append((lineStrip.split('|'))[0].strip())
        topicsCommon.append((lineStrip.split('|'))[1].strip())
    else:
        if ((lineStrip.strip())[0] == "_"):
            topics.append("\\textbf{" + (lineStrip.strip())[1:] + "}")
        else:
            topics.append(lineStrip.strip())
        topicsCommon.append("")
#=====================
# Create calendar
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
# Create names of free days

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


#=====================
# Output

outputGenCalendar = ""
for i in range(6):
    outputGenCalendar+=lines[i]

outputGenCalendar+="N;\tWeek;\tWeekAB;\tDate;\tFreeDay;\tDoW;\tHrs;\tTopic\n" 
outputTEX='\n\
\documentclass[DIV15, 12pt,a4paper]{scrartcl}\n\
\usepackage{xltxtra}\n\
\usepackage{fontenc}\n\
\n\
\usepackage[ngerman]{babel}\n\
\usepackage{graphicx}\n\
\usepackage{lmodern}\n\
\usepackage{amsmath}\n\
\usepackage{units}\n\
\usepackage{nicefrac}\n\
\usepackage{SIunits}\n\
\usepackage{ucs}\n\
\usepackage{algorithmic}\n\
\usepackage[table,svgnames]{xcolor}\n\
\usepackage{placeins}\n\
\usepackage{fancyhdr}\n\
\usepackage{indentfirst}\n\
\usepackage{lastpage}\n\
\usepackage{enumerate}\n\
\usepackage{hyperref}\n\
\usepackage{longtable}\n\
\usepackage{tabu}\n\
\n\
\pagestyle{fancy}\n\
\n\
\n\
\lhead{%s %sKl, 2014/2015}\n\
\n\
\\begin{document}\n\
  \\begin{longtabu} to \linewidth {|l|l|X|l|}\n\
    \\rowfont\\bfseries \n\
    \hline\n\
      Wo. & Datum & Thema des Unterrichtes   &  Std.  \\\\ \n\
    \hline\n\
    \hline\n\
    \endhead\n'%(Title, Class)

topicId = 0
WeekN = 1
WeekAB = 'a'
Hrs = 0
colorWeek = '\cellcolor{black!5}'
colorWeekCur = ''

for i in range(len(createdCal)):
    if ((topicId<len(topics)) and (topicsCommon[topicId]<>"")):
        outputTEX+="\multicolumn{3}{|c|}{\\textbf{%s}} & \\textbf{%s} \\\\ \n\
    \hline\n"%(topics[topicId], topicsCommon[topicId])
        topicId+=1
        continue
    if (i<>0 and createdCal[i].isocalendar()[1] <> createdCal[i-1].isocalendar()[1]):
        WeekN+=1
        if (WeekAB=='a'):
            WeekAB='b'
            colorWeekCur = colorWeek
        else:
            WeekAB='a'
            colorWeekCur = ''
    FreeDay=""
    if createdCalNames[i]<>"":
        FreeDay="F"
    else:
        FreeDay="-"
        Hrs+=1
    outputGenCalendar+="%d;\t%d;\t%s;\t%s;\t%s;\t%s;\t%d;\t%s;\t;\n"%(i+1,
        WeekN, WeekAB, createdCal[i], FreeDay, DayOfWeek(createdCal[i].isocalendar()[2]),
        Hrs, createdCalNames[i])
    
    
    if (createdCalNames[i]<>""):
        outputTEX+="%s%s%s & \cellcolor{blue!15}%d/%d/%d, %s & \cellcolor{blue!15}%s & - \\\\ \n    \hline\n    "%(
            WeekN,WeekAB,colorWeekCur,createdCal[i].day,createdCal[i].month,createdCal[i].year,DayOfWeek(createdCal[i].isocalendar()[2]),createdCalNames[i])
    elif (topicId<len(topics) and createdCalNames[i]==""):
        outputTEX+="%s%s%s & %d/%d/%d, %s & %s & %d \\\\ \n    \hline\n    "%(
            WeekN,WeekAB,colorWeekCur,createdCal[i].day,createdCal[i].month,createdCal[i].year,DayOfWeek(createdCal[i].isocalendar()[2]),topics[topicId],Hrs)
        topicId+=1
     

outputTEX+="\end{longtabu}\n\
\end{document}"

#file(sys.argv[1]+'.gencalendar','w').write(outputGenCalendar)
file(sys.argv[1]+'.tex','w').write(outputTEX)

os.system('xelatex ' + sys.argv[1]+'.tex')
os.system('xelatex ' + sys.argv[1]+'.tex')
subprocess.Popen(['evince', sys.argv[1]+'.pdf'])
