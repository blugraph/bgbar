
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
RUN_DIR = "/home/pi/dev/files/"
#RUN_DIR = "/media/files/"

private_key = "lx_sg1.pem"
svc_url1 = "http://" + SERVER_ADDR + "/blunois/transfercompleted.php"
while 1:


	payload=[{"FileName":"2016-05-13_16_20_54.wav","stationID":stationID}]                                                              
	r1 = requests.put(svc_url1, data=json.dumps(payload), timeout=0.1)
	print r1.status_code						
	if r1.status_code==200:
									
    		print "Successfully acknowledged"									
                                                                
	else:
	 			
                                                                       
		print "Could not complete the transfer update"
	time.sleep(2)	
