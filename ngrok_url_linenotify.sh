#!/bin/bash
sudo kill $(pidof ngrok)
ngrok http --host-header=localhost 631 > /dev/null& 
sleep 3
#取得執行結果(位址)當變數
URL4040=$(curl -s localhost:4040/api/tunnels | awk -F"https" '{print $2}' | awk -F"//" '{print $2}' | awk -F'"' '{print $1}')
ACCESS_TOKEN="6RHZXwSH8bVgEWjIPakc6nkNLxQ4qZlaXJvm8Cwx1Co" #Line Notify 的驗證碼
message="CUPS url https://"$URL4040  #傳入影像檔的路徑
echo $URL4040 > ngrok_url.txt
curl https://notify-api.line.me/api/notify -X POST \
   -H "Authorization: Bearer $ACCESS_TOKEN" \
   -F "message=$message"  
