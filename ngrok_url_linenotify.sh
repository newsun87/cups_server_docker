#!/bin/bash
sudo kill $(pidof ngrok)
ngrok http --host-header=localhost 631 > /dev/null& 
sleep 3
#���o���浲�G(��})���ܼ�
URL4040=$(curl -s localhost:4040/api/tunnels | awk -F"https" '{print $2}' | awk -F"//" '{print $2}' | awk -F'"' '{print $1}')
ACCESS_TOKEN="6RHZXwSH8bVgEWjIPakc6nkNLxQ4qZlaXJvm8Cwx1Co" #Line Notify �����ҽX
message="CUPS url https://"$URL4040  #�ǤJ�v���ɪ����|
echo $URL4040 > ngrok_url.txt
curl https://notify-api.line.me/api/notify -X POST \
   -H "Authorization: Bearer $ACCESS_TOKEN" \
   -F "message=$message"  
