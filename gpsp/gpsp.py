import gps, os, time
from collections import defaultdict
import os
from gps import *
from time import *
import time
import threading
import requests

paramNameList = [
'gpsstatus',
'station_id',
'latt',
'long',
'time'
]

fortime=" "

TIMEZ = 8

def spliting(s, chunk_size):
    a = zip(*[s[i::chunk_size] for i in range(chunk_size)])
    return [''.join(t) for t in a]


gpsvals = {}

gpsd = None #seting the global variable

#os.system('clear') #clear the terminal (optional)

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
i=1

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
      gpsp.start() # start it up
      for i in range (1,6):
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc

#      os.system('clear')

      	print
      	print ' GPS reading'
      	print '----------------------------------------'
      	print 'latitude    ' , gpsd.fix.latitude
      	print 'longitude   ' , gpsd.fix.longitude
      	print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
#      print 'time utc    ' , gpsd.time
      	print 'altitude (m)' , gpsd.fix.altitude
      	print 'eps         ' , gpsd.fix.eps
      	print 'epx         ' , gpsd.fix.epx
      	print 'epv         ' , gpsd.fix.epv
      	print 'ept         ' , gpsd.fix.ept
      	print 'speed (m/s) ' , gpsd.fix.speed
      	print 'climb       ' , gpsd.fix.climb
      	print 'track       ' , gpsd.fix.track
      	print 'mode        ' , gpsd.fix.mode
	time.sleep(2)

      if gpsd.utc != None and gpsd.utc != '':
        tzhour = int(gpsd.utc[11:13])+TIMEZ
        if (tzhour>23):
          tzhour = (int(gpsd.utc[11:13])+TIMEZ)-24
        gpstime = gpsd.utc[0:4] + gpsd.utc[5:7] + gpsd.utc[8:10] + ' ' + str(tzhour) + gpsd.utc[13:19]	
        print 'Setting system time to GPS time...'
        print gpstime
	d,t1=gpstime.split(" ")
        y,md=spliting(d,4)
	m,s=spliting(md,2)
	fortime= str(y)+"/"+str(m)+"/"+str(s)+" "+str(t1)
	print "formatter time"
	print fortime      
# added -u to set clock to UTC time and not effect the timezone
        s=os.system('sudo date  --set="%s"' % gpstime)	
	print s

      if ((gpsd.fix.latitude==0.0) or (gpsd.fix.longitude==0.0) or (gpsd.fix.latitude==" ") or (gpsd.fix.longitude==" ")):
        paramName = paramNameList[0]
        gpsvals[paramName] = "NO"
      else:
        paramName = paramNameList[0]
        gpsvals[paramName] = "YES"

      paramName = paramNameList[1]
      gpsvals[paramName] = "N1001"
      paramName = paramNameList[2]	
      gpsvals[paramName] = str(gpsd.fix.latitude)
      paramName = paramNameList[3]
      gpsvals[paramName] = str(gpsd.fix.longitude)
      paramName = paramNameList[4]
      gpsvals[paramName] = fortime

      abs_file_name= "cordinates.txt"
      try:
        f = open(abs_file_name, 'w')
        print>>f, json.dumps(gpsvals)
      #del gpsvals[:]
      except:
        print ": Failed to create file"
      
      try:
      	gpsjson = '[' + json.dumps(gpsvals) + ']'
    	r1 = requests.put("http://52.74.191.39/blunois/gpsupdate.php", gpsjson, timeout=0.1)
    	print r1.status_code
    	print r1.content
      except Exception as x:
    	print "Network Failed Error:", x

#      sleep(5)	

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
  gpsp.running = False
