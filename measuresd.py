import time
from datetime import datetime
import RPi.GPIO as GPIO
import requests
import json
import serial
import os
import struct
import sys

import gps, os, time

import pyaudio
import wave

stationID="N1001"

lf=0x0A

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WIDTH = 2
rec=0 # To indicate that a recording has started
livefile=0 # To indicate that a file info not updated to server is available now
fltr=0 # To Indicate that a file avaialble to transfer to is available now 

BACKLOG_BUFF_LEN=999

tofile=[]

lps_int=1
leq_int=10

SEND_LOOP=60

noswals={}

network_send="Off"

def sysinit():
	global network_send
	try:
                        print "In the settings loop"
                        r2 = requests.put("http://52.74.191.39/blunois/stationdata.php",data="N1001")
                        print (r2.content)
                        data = json.loads(r2.content)
                        # Settings for data capture"
                        if data[3]=="100ms":
                                lps_int=.1
                        elif data[3]=="200ms":
                                lps_int=.2
                        elif data[3]=="1s":
                                lps_int=1
                        elif data[3]=="Leq1s":
                                lps_int=1
                        else :
                                lps_int=100

                        if data[0]=="Off":
                                leq_int=100
                        elif data[0]=="10s":
                                leq_int=10
                        elif data[0]=="1m":
                                leq_int=60
                        elif data[0]=="5m":
                                leq_int=300
                        elif data[0]=="10m":
                                leq_int=600
                        elif data[0]=="30m":
                                leq_int=1800
                        elif data[0]=="1h":
                                leq_int=3600
                        elif data[0]=="8h":
                                leq_int=28800
                        elif data[0]=="24h":
                                leq_int=86400
                        elif data[0]=="Manual":
                                leq_int=data[0]

                        ser1.write("Output Level Range Upper,")
                        ser1.write(data[10])
                        ser1.write('\r\n')
                        time.sleep(.2)
                        ser1.write("Output Level Range Lower,")
                        ser1.write(data[11])
                        ser1.write('\r\n')
                        time.sleep(.2)
                        ser1.write("Frequency Weighting,")
                        ser1.write(data[9])
                        ser1.write('\r\n')
                        time.sleep(.2)
                        ser1.write("Time Weighting,")
                        ser1.write(data[12])
                        ser1.write('\r\n')
                        time.sleep(.2)
#                        ser1.write("Ly Type,")
#                        ser1.write(data[13])
#                       ser1.write("Lpeak")

#                        ser1.write('\r\n')
#                        time.sleep(.2)
                        ser1.write("TRM,")
                        ser1.write(data[19])
                        ser1.write('\r\n')
                        time.sleep(.2)
                        ser1.write("Diffuse Sound Field Correction,")
                        ser1.write(data[8])
                        ser1.write('\r\n')
                        time.sleep(1)
                        ser1.write("Delay Time,")
                        ser1.write(data[20])
                        ser1.write('\r\n')
                        ser1.write("Back Erase,")
                        ser1.write(data[21])
                        ser1.write('\r\n')
                        network_send=data[22] #to see if send over or store locally 
                        time.sleep(2)
			print "The network flag is "+network_send
			time.sleep(.5)
                        while ser1.inWaiting() > 0:
                                out += ser1.read(1)
                        print out
#                        time.sleep(2)
	except:
                        print "No Network avavailable"
                        print "Unexpected error:", sys.exc_info()[0]
	return


ser1 = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=2)
print ser1
ser1.flushInput()

# Setting Clock 

fl='/home/pi/dev/gpsp/cordinates.txt'
with open(fl,'r') as f:
        tofile_json = f.read()
data=json.loads(tofile_json)

if data["gpsstatus"]=="YES":
#	tnow = time.strftime("%Y/%m/%d %H:%M:%S")
	tnow=data["time"]
	print tnow
	ser1.write("Clock,")
	ser1.write(tnow)
	ser1.write('\r\n')
	print "gps is on now"
	time.sleep(.5)
	out=" "
        while ser1.inWaiting() > 0:
                out += ser1.read(1)
        print out
        time.sleep(.5)
        out=" "
else:
	print "gps is not on"
	ser1.flushInput()
	ser1.write("Clock?")
        ser1.write('\r\n')
	time.sleep(.5)
	out=" "
	while ser1.inWaiting() > 0:
        	out += ser1.read(1)
        print out
	td= out.splitlines(1)[1]
	d,t=td.split(" ")
	y,m,d1=d.split("/")
	devtime=str(y)+str(m)+str(d1)+" "+str(t)
	print "New Dev Time formatted"
	print devtime
	print "Updating System Time with device Time"
	os.system('sudo date  --set="%s"' % devtime)
        time.sleep(.5)
	out=" "

ser1.flushInput()
time.sleep(.5)
print "Device current  time"
ser1.write("Clock?")
ser1.write('\r\n')
time.sleep(.5)
out=" "
while ser1.inWaiting() > 0:
        out += ser1.read(1)
time.sleep(.5)
out=" "

time.sleep(2)

# Displays switched ON 
ser1.write("Display Sub Channel,On")
ser1.write('\r\n')
time.sleep(.2)
ser1.write("Display Ly,On")
ser1.write('\r\n')
time.sleep(.2)
ser1.write("Display Leq,On")
ser1.write('\r\n')
time.sleep(.2)
ser1.write("Display LE,On")
ser1.write('\r\n')
time.sleep(.2)
ser1.write("Display Lmax,On")
ser1.write('\r\n')
time.sleep(.2)
ser1.write("Display Lmin,On")
ser1.write('\r\n')
time.sleep(.2)
ser1.write("Display LN1,On")
ser1.write('\r\n')
time.sleep(.2)
ser1.write("Display LN2,On")
ser1.write('\r\n')
time.sleep(.2)
ser1.write("Display LN3,On")
ser1.write('\r\n')
time.sleep(.2)
ser1.write("Display LN4,On")
ser1.write('\r\n')
time.sleep(.2)
ser1.write("Display LN5,On")
ser1.write('\r\n')
time.sleep(.2)
ser1.write("AC OUT, Main")
ser1.write('\r\n')
time.sleep(2)
ser1.flushInput()

out = ' '
set=0
man=0
auto=0
measure=0
meas_int=1
while 1:
# This is to start the measurement, recording and upload files 
	noise = ' '
	out= ' ' 
	try:
#		ser1.flushInput()
		if auto==0: # If web record on, auto = 1 and no check for manual button required. Web recording can not be stopped manually 
            		
			ser1.flushInput()
		    	time.sleep(.5)
            		print "Measurement Button ? "
            		ser1.write("Measure?")
            		ser1.write('\r\n')
            		time.sleep(1)
            		out=" "
            		while ser1.inWaiting() > 0:
               			out += ser1.read(1)
            		time.sleep(.5)
            		print out
            		button=(out.splitlines(1)[1]).rstrip('\r\n') # This removes the additional characters of /r/n present in the string for new line and CF. 
            		out=" "
            		print "The state of the start button"
            		print "****"+button+"***" 
			if button=="Start":
				man=1
				print "Manual Measurement ON"
			elif button=="Stop":
				man=0
				print "Manual measurement switched off"	
			print "Value of man"
			print man
            	r3 = requests.put("http://52.74.191.39/blunois/stationaction.php", data=stationID)
            	data = json.loads(r3.content)
            	print (r3.content)
        	if data[0] == "1":
		  auto=1
		  print "Measure Button Pressed"		  
		  if set==0: # set parameters for the first time
			  set=1
			  sysinit() # This function reads the device config information from web
		  if lps_int==100 and leq_int==100:
		    print "No Measurement Needs to be done - Both Intervals are turned off"	
		    measure=0
		  else:
			if lps_int < leq_int:
	            		meas_int=lps_int
		    		measure=1
		  	else:
		    		meas_int=leq_int
		    		measure=1
                        ser1.write("Measure,Start")
                        ser1.write('\r\n')
                  	print "The measurement Interavel is :"+str(meas_int)+"s"
			while ser1.inWaiting() > 0:
                                out += ser1.read(1)
                        print out

                elif man==0 and auto==1: # Here the web info is 0
		
                        print "Manual  Measurements Released"
                        auto=0
			measure=0	
                        set=0
                        ser1.write("Measure,Stop")
                        ser1.write('\r\n')
                        time.sleep(.5)
                        discard=' '
                        while ser1.inWaiting() > 0:
                                discard += ser1.read(1)
		else:

			print "All Measurements Released"
                        auto=0
                        measure=0
			set=0

 		if measure==1 or man==1:
			meas_star_time=time.time()
		    	while ((time.time() - meas_star_time) < SEND_LOOP) or (time.time() - meas_star_time) < meas_int:	
				ser1.flushInput()
	                        ser1.write("DOD?")
        	                ser1.write('\r\n')
				time.sleep(meas_int)
		                while ser1.inWaiting() > 0:
                	                out += ser1.read(1)
#				print out
			        try:
        	                       	noise= out.splitlines()[1]
#					print "++++++"	
					print noise
#					print "++++++"
					ser1.flushInput()
					i = time.strftime("%Y-%m-%d %H:%M:%S")
                                	print (i)
                                	payload = {"deviceID":"N1001", "noise": noise, "time":i}                                        
                                	tofile.append(payload)
	                        except:
               		               print "No Response from the Machine"
				out=' '
				noise=' '
				#time.sleep(meas_int) 
			if (len(tofile))>0:	
                		print "At least one data in the making"
				print network_send
				if network_send=="On": # This is Auto, checking if network optin is selected or not 
					print "Lets send to network"
					try:
						r1 = requests.put("http://52.74.191.39/blunois/noisedata.php", data=json.dumps(tofile), timeout=0.1)
		                		print r1.status_code,": server response."
	       		        		print r1.content
	        			except:
        	        			print ": Network Failed while uploading data buffer:"	  
				if auto==0: # This means it is manual recording. If manual and auto on, then it will send file anyways. 
                                        dir_name= "/media/BGBAR/measure/manual/"+time.strftime("%Y-%m-%d_%H")
				else:	
					dir_name= "/media/BGBAR/measure/"+time.strftime("%Y-%m-%d_%H")
           			try:
               				os.makedirs(dir_name)
         			except OSError:
                			if os.path.exists(dir_name):
                        			print ": Already directory exists"
                			else:
                        			print ": Some system Error in creating directory"
     			        	print ": Failed creating the directory"
	            		try:
           				fname=os.path.join(dir_name, "measurement" + "." + "txt")
					if not os.path.isfile(fname):
						print "File created first time"
						with open(fname, mode='w') as f:
       							f.write(json.dumps(tofile, indent=2))
					else:
						print "File already here"	
    						with open(fname) as feedsjson:
       							feeds = json.load(feedsjson)
   							feeds.append(tofile)
    							with open(fname, mode='w') as f:
       								f.write(json.dumps(feeds, indent=2))
				except:
					print "File can not be written to the drive"
				del tofile[:]				

	except (KeyboardInterrupt, SystemExit):
			
		ser1.write("Measure,Stop")
       		ser1.write('\r\n')
                print "No Network avavailable"
                print "Unexpected error:", sys.exc_info()[0]	
		exit()



