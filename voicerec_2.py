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

#Program the number of seconds to record here
secs=1800

lf=0x0A

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WIDTH = 2
rec=0 # To indicate that a recording has started
livefile=0 # To indicate that a file info not updated to server is available now
fltr=0 # To Indicate that a file avaialble to transfer to is available now 

BACKLOG_BUFF_LEN=59


def callback(in_data, frame_count, time_info, status):
        frames.append(in_data)
        return (in_data, pyaudio.paContinue)

noswals={}

p = os.popen("df -h /")
i = 0
for i in range (1, 3):
        line = p.readline()
        if i==2:
                disk_space= (line.split()[3])
out = ' '
recordID=' '
livefile=0

while 1:
# This is to start the measurement, recording and upload files 
	noise = ' '
	out= ' ' 
	try:
#		ser1.flushInput()
		
		r3 = requests.put("http://52.74.191.39/blunois/stationaction.php",data="N1001")
		data = json.loads(r3.content)
		print (r3.content)
		if data[1]=="1":
			if rec==0: # This is recording setup and start recording for the first time 
				print "Record Button Pressed"
				r5=requests.put("http://52.74.191.39/blunois/getrec_scheduleid.php",data="N1001") # Requests for the record ID 
                        	data5 = json.loads(r5.content)
                        	print (r5.content)
                        	recordID=data5[0]
                        	print (recordID)	
				rec=1
#				dir_name= "/home/pi/dev/files"
#				dir_name= "/media/BGBAR/voice/"+time.strftime("%Y-%m-%d")
				dir_name= "/media/BGBAR/voice"
            			try:
	               			os.makedirs(dir_name)

            			except OSError:
                			if os.path.exists(dir_name):
                        			print "Directory Already exists"
                			else:
                        			print "Some system Error in creating directory"

		                	print " Failed creating the directory"

	            		try:	
					start_time=time.time()
					p = pyaudio.PyAudio()
                                        frames = []
                                        stream = p.open(format=FORMAT,
                                                channels=CHANNELS,
                                                rate=RATE,
                                                input=True,
                                                frames_per_buffer=CHUNK,
                                                stream_callback=callback)

			    	except:
	              			print "Failed to create file or the py audio failed"
			else: 	# Call back function on recording on, there is nothing to be done
				time.sleep(1)
				print("* recording")
			
			curr_time=time.time() # This is for intermediate file writing for every secs, defined on this file. 
                        if (curr_time-start_time)>secs:
				print curr_time-start_time
				print "New file created"
				start_time=curr_time
                                base_filename=(time.strftime("%Y-%m-%d_%H_%M_%S")+"." + "wav")
                                abs_file_name=os.path.join(dir_name, base_filename)
                                wf = wave.open(abs_file_name, 'wb')
				
				wf.setnchannels(CHANNELS)
                                wf.setsampwidth(p.get_sample_size(FORMAT))
                                wf.setframerate(RATE)
                                wf.writeframes(b''.join(frames))
                                wf.close()
				livefile=1
				del frames[:]					

		else: # This indicates recording has stopped 
			
			if rec==1: # Recording has stopped, now save the file and indicate there is a live file. 
				base_filename=(time.strftime("%Y-%m-%d_%H_%M_%S")+"." + "wav")
                                abs_file_name=os.path.join(dir_name, base_filename)
                                wf = wave.open(abs_file_name, 'wb')
				print "New file created"	
				rec=0
				print "Record Released"
				stream.stop_stream()
				stream.close()
				p.terminate()
				wf.setnchannels(CHANNELS)
				wf.setsampwidth(p.get_sample_size(FORMAT))
				wf.setframerate(RATE)
				wf.writeframes(b''.join(frames))
				wf.close()
				livefile=1
				del frames[:]
	            
		if livefile==1: # There is a file to transfer
				print "Trasnferring file info"
				payload = [{"FileName":base_filename, "stationID":stationID, "StorageSpace":disk_space,"RecScheduleID":recordID}]
				r4 = requests.put("http://52.74.191.39/blunois/recordvoice.php",data=json.dumps(payload))
	                       	print (r4.content)
				livefile=0
		else:
				print "Record activity Inactive "
				time.sleep(1)

	except (KeyboardInterrupt, SystemExit):
			
			ser1.write("Measure,Stop")
        		ser1.write('\r\n')
                        print "No Network avavailable"
                        print "Unexpected error:", sys.exc_info()[0]	
			exit()
	
# This is to start the recording

