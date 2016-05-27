import time
from datetime import datetime
import RPi.GPIO as GPIO
import requests
import json
import serial
import struct
import sys
import os
import time
from os import listdir
from os.path import isfile, join
import glob, os
import requests
import cPickle as pickle
import gps, os, time
import pysftp
import pyaudio
import wave

stationID="N1001"

file_list_local = []
file_list_target = []
SERVER_ADDR = "52.74.191.39"
#RUN_DIR = "/home/pi/dev/files/"
RUN_DIR = "/media/BGBAR/voice/"

private_key = "/home/pi/dev/files/lx_sg1.pem" 

dir_name = RUN_DIR

os.chdir(dir_name)
for file in glob.glob("*.wav"):
	file_list_local.append(file)

print "There are " + str(len(file_list_local)) + " files in the directory"

#print file_list_local
#while 1:
try:
	r3 = requests.put("http://52.74.191.39/blunois/stationaction.php",data="N1001")
        data = json.loads(r3.content)
        print (r3.content)
        if data[2]=="1":
		print "Upload  Button Pressed"
                r5 = requests.put("http://52.74.191.39/blunois/voicesend.php",data="N1001")
                file_list = json.loads(r5.content)
		print file_list 

		for j in range(0, len(file_list_local)):
			for k in range(0, len(file_list)):
				if file_list[k]==file_list_local[j]:
					print "matched"	
					file_list_target.append(file_list[k])
		print file_list_target	

		if len(file_list_target) == 0:
			print "There are no matching files"
		else:
			print "There are matching files"	
			srv = pysftp.Connection(host="52.74.191.39", username="ubuntu", private_key=private_key)
			print srv
                        srv.chdir('/var/www/html/blunois/audio_file/')
			print "Remote working "
			for k in range(0, len(file_list_target)):
					print "Sending the file now"
					srv.put(file_list_target[k])
                                        print "Successfully updated the transfer"

					try:	
							print "Successfully sent the file, deleting now"
          						os.remove(file_list_target[k])
							try:
								svc_url1 = "http://" + SERVER_ADDR + "/blunois/transfercompleted.php"
								payload=[{"FileName":file_list_target[k],"stationID":stationID}]
								r1 = requests.put(svc_url1, data=json.dumps(payload), timeout=0.1)
                                        			print r1.status_code
								if r1.status_code==200:
									print "Successfully acknowledged"
								else:
									print "Could not complete the transfer update"
							except:
								print "Network failure on status update"		
        				except OSError, e:  ## if failed, report it back to the user ##
  		          				print ("Error: %s - %s." % (e.filename, e.strerror))
	else:
		print "No files to upload"
except:
	print "Some failure"
#	time.sleep(5)
