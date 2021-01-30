#!/bin/bsah
r1=`hostname -I`
r2=`iwconfig wlan0 | grep wlan0 | awk -F '"'  '{print $2}'`
r3=`lpstat -p -d | grep system | awk -F ' '  '{print $4}'`
r4=`cat ngrok_url.txt`
printf '{"hostname":"%s","ap":"%s","queuename":"%s","ngrok_url":"%s"}\n' "$r1" "$r2" "$r3" "$r4"> config.json
