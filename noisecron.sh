#! /bin/bash

case "$(pgrep -f measuresd.py | wc -w)" in

0)  echo "Starting Noise"
#    sudo gpsd -F /var/run/gpsd.sock /dev/ttyAMA0
    sudo /home/pi/cl/Record_from_lineIn.sh

    sudo python /home/pi/dev/measuresd.py
    ;;
*)  echo "Noise  already running"
    ;;
esac

