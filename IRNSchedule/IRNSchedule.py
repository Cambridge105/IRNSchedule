from crontab import CronTab
from datetime import datetime
from datetime import timedelta
from croniter import croniter
from dateutil import rrule


file = open('irn.html', 'w')
my_user_cron = CronTab(tabfile='crontab-copy')

now = datetime.now()
next_hour = datetime(now.year, now.month, now.day, now.hour, 0)

sevenDaysLater = now + timedelta(days=7)
file.write("<html><head><title>Cambridge 105 - IRN scheduling</title></head><body><h1>IRN TOTH Schedule</h1><p>Generated at: ")
file.write(now.strftime("%H:%M on %d %b %Y"))
file.write("</p><table border=\"1\"><thead><tr><th>Hour</th><th>Schedule</tr></thead><tbody>")

for dt in rrule.rrule(rrule.HOURLY, dtstart=next_hour, until=sevenDaysLater):
    hours = dt+timedelta(hours=1)
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

    hoursStr = hours.strftime("%a %d %b %Y %H:%M")
    if (" on on " in hourCmd):
        hourCmd = "IRN, weather-next"
    if (" on off " in hourCmd):
        hourCmd = "IRN only"
    if (" on flp " in hourCmd):
        hourCmd = "IRN, weather-now"
    if (minsOffset > 59):
        hourCmd = "-"
    file.write("<tr><td>"+ hoursStr+"</td><td>"+ hourCmd+"</td></tr>")
file.write("</tbody></table>")
file.close()