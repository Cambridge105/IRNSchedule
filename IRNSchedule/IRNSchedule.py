from crontab import CronTab
from datetime import datetime
from datetime import timedelta
from croniter import croniter
from dateutil import rrule


file = open('/home/pi/105irnschedule/irn.html', 'w')
my_user_cron = CronTab(tabfile='/home/pi/105irnschedule/crontab')

now = datetime.now()
next_hour = datetime(now.year, now.month, now.day, now.hour, 0)

sevenDaysLater = now + timedelta(days=7)
file.write("<html><head><title>Cambridge 105 - IRN scheduling</title>\r\n")
file.write("<style>\r\n.irn {background-color:GoldenRod;}\r\n.none {background-color:LightCoral;}\r\n.unknown {background-color:LightGrey;}\r\n</style>")
file.write ("</head><body><h1>IRN TOTH Schedule</h1><p>Generated at: ")
file.write(now.strftime("%H:%M on %d %b %Y"))
file.write("</p>\r\n")

print("Working on rules...")
lastday = -1
currentday = now.strftime("%W")
hasToday = False
todayOutput = ""

for dt in rrule.rrule(rrule.HOURLY, dtstart=next_hour, until=sevenDaysLater):
    hours = dt+timedelta(hours=1)
    currentday = hours.strftime("%w")
    if (currentday != lastday):
        if (lastday != -1):
            file.write ("</tbody></table>\r\n")
			hasToday = True
        file.write ("<h2>" + hours.strftime("%a %d %b %Y") + "</h2>")
        file.write ("\r\n<table border=\"1\"><thead><tr><th>Hour</th><th>Schedule</tr></thead><tbody>")
    hasResult = False
    nextDate = sevenDaysLater
    hourCmd = ""
    minsOffset = 0
    for job in my_user_cron:
       if ("switchirn" in job.command):
           if (hasResult == False):
              sch = job.schedule(date_from=dt)
              nextSched = sch.get_next() + timedelta(minutes=10)
              if (nextSched < nextDate):
                  nextDate = nextSched
                  dateOffset = nextDate - hours
                  minsOffset = dateOffset.seconds/60
                  hourCmd = job.command
                  if ("NEWSONWED" in job.command):
                      hourCmd = "(Depends on NEWSONWED setting)"
                      rowclass="unknown"

    hoursStr = hours.strftime("%H:%M")
    if (" on on " in hourCmd):
        hourCmd = "IRN, weather-next"
        rowclass = "irn"
		if (hasToday == False):
		    todayOutput = todayOutput + hoursStr + ", "
    if (" on off " in hourCmd):
        hourCmd = "IRN only"
        rowclass="irn" 
		if (hasToday == False):
		    todayOutput = todayOutput + hoursStr + ", "
    if (" on flp " in hourCmd):
        hourCmd = "IRN, weather-now"
        rowclass="irn"
		if (hasToday == False):
		    todayOutput = todayOutput + hoursStr + ", "
    if (minsOffset > 59):
        hourCmd = "-"
        rowclass="none"
    file.write("<tr class=\"" + rowclass + "\"><td>"+ hoursStr+"</td><td>"+ hourCmd+"</td></tr>\r\n")
    lastday = hours.strftime("%w")
file.write("</tbody></table>")
print("Done")
print(todayOutput)
file.close()