import os
import time
from os import listdir
from os.path import isfile, join
import glob, os
import requests
import json

fl='/home/pi/dev/gpsp/cordinates.txt'
with open(fl,'r') as f:
	tofile_json = f.read()
data=json.loads(tofile_json) 

print data
print data["gpsstatus"]

