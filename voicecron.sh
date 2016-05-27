#! /bin/bash

case "$(pgrep -f voicerec_2.py | wc -w)" in

0)  echo "Starting Voice Record"
    sudo python /home/pi/dev/voicerec_2.py
    ;;
*)  echo "Voice Rec  already running"
    ;;
esac


