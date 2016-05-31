import os
import time
import requests
import json
from collections import namedtuple

disk_ntuple = namedtuple('partition',  'device mountpoint fstype')
usage_ntuple = namedtuple('usage',  'total used free percent')

def disk_partitions(all=False):
    """Return all mountd partitions as a nameduple.
    If all == False return phyisical partitions only.
    """
    phydevs = []
    f = open("/proc/filesystems", "r")
    for line in f:
        if not line.startswith("nodev"):
            phydevs.append(line.strip())

    retlist = []
    f = open('/etc/mtab', "r")
    for line in f:
        if not all and line.startswith('none'):
            continue
        fields = line.split()
        device = fields[0]
        mountpoint = fields[1]
        fstype = fields[2]
        if not all and fstype not in phydevs:
            continue
        if device == 'none':
            device = ''
        ntuple = disk_ntuple(device, mountpoint, fstype)
        retlist.append(ntuple)
    return retlist

def disk_usage(path):
    """Return disk usage associated with path."""
    st = os.statvfs(path)
    free = (st.f_bavail * st.f_frsize)
    total = (st.f_blocks * st.f_frsize)
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    try:
        percent = ret = (float(used) / total) * 100
    except ZeroDivisionError:
        percent = 0
    # NB: the percentage is -5% than what shown by df due to
    # reserved blocks that we are currently not considering:
    # http://goo.gl/sWGbH
    return usage_ntuple(total, used, free, round(percent, 1))
sd={}
paramList = [
'diskyn',
'disktotal',
'diskfree'
]

sd[paramList[0]]="NO"
sd[paramList[1]]="0"
sd[paramList[2]]="0"
diskfree=str("0")
disktotal=str("0")
diskyn="NO"
if __name__ == '__main__':
    for part in disk_partitions():
	print part 
        if part.mountpoint=="/media/BGBAR":
		diskyn="YES"
		sd[paramList[0]]="YES"	
		if sd[paramList[0]]=="YES":
			diskdet=str(disk_usage(part.mountpoint))
			disktotal=(str((disk_usage(part.mountpoint).total)/1000000))
			diskfree=(str((disk_usage(part.mountpoint).free)/1000000))
	        	print "    %s\n" % diskdet, diskfree, disktotal
			sd[paramList[1]]=str(disktotal)
			sd[paramList[2]]=str(diskfree)
		else:
			diskfree=str("0")
			diskyn="NO"
			disktotal=str("0")

		f = open('sdfilesize.txt', 'w')
		f.write(json.dumps(sd))
        	f.close()
    try:	
		i = time.strftime("%Y-%m-%d %H:%M:%S")
		print i 
        	payload = [{"deviceID":"N1001", "disk":diskyn, "Total":disktotal,"Free":diskfree,"time":i}]
        	print "Send Data to server"
      		r1 = requests.put("http://52.74.191.39/blunois/sdcardstatus.php", data=json.dumps(payload))
       		print r1.status_code
    except:	
		print "Server Error"
