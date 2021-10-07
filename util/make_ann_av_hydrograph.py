from HydrographTools import *
from pylab import *
import pdb

siteno = [13337000,13336500]
statid = '735:ID:SNTL'
stat_name = 'Savage Pass Snotel'
#df = ImportUsgsSiteDailyValues(siteno)
#dvstat = GetDailyStats(df)
#plot(dvstat.date,dvstat.value)
#show()
#MakeAnAvHydrograph(siteno)


#make figure
fig, ax = plt.subplots()
try:
    num = len(siteno)
except TypeError:
    siteno = [siteno]

ax2 = ax.twinx()

swe = ImportSnotel(statid)
swe_a= GetDailyStats(swe)
swe_line = ax2.plot(swe_a.index,swe_a.value,'r--',lw=2,label=stat_name)

lns = swe_line

for i in xrange(len(siteno)):    
    df,siteinfo = ImportUsgsSiteDailyValues(siteno[i])
    dvstat = GetDailyStats(df)
    lname = ax.plot(dvstat.index, dvstat.value,lw=2,label=siteinfo['name'])
    lns = lns + lname

labs = [l.get_label() for l in lns]

months = mdates.MonthLocator()   # every month
monthsFmt = mdates.DateFormatter('%b')
## format the ticks
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
# set limits
datemin = dt.date(dvstat.index.min().year, 10, 1)
datemax = dt.date(dvstat.index.max().year, 9, 30)
ax.set_xlim(datemin, datemax)

# format the coords message box
def cfs(x):
    return '%1.2f' % x
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.format_ydata = cfs
ax.grid(True)
ax.legend(lns,labs,loc='best')
ax.set_ylabel('Discharge (cfs)')
ax2.set_ylabel('Snow Water Equiv. (in.)')

fig.autofmt_xdate()
plt.show()
