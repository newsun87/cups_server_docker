# -*- coding: UTF-8 -*-
from flask import Flask, request, abort, render_template
import requests
import json
import os, shutil
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import subprocess
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time
import configparser
import mimetypes
import paho.mqtt.client as mqtt

config = configparser.ConfigParser()
config.read('cups_printer.conf')

#取得通行憑證
cred = credentials.Certificate("serviceAccount.json")
database_url = config.get('firebase', 'database_url')
firebase_admin.initialize_app(cred, {
    'databaseURL' : database_url
})

ref = db.reference('/') # 參考路徑
cups_ref=ref.child('line-printer-bot/cups0001')

app = Flask(__name__)

@app.route('/')
def showPage(): # 顯示網頁
 return "Hello CUPS!"
    
def download_gdrive_print():
  #目前所在絕對路徑
  basepath = os.path.dirname(__file__)
  gauth = GoogleAuth()
  #gauth.CommandLineAuth() #透過授權碼認證
  drive = GoogleDrive(gauth)  
  try:      
    # 取得 gdrive 檔案清單
    file_list1 = drive.ListFile({'q': "'135y-D-jDEh-Bub_WpjmhYxWxJkUyPmUr' in parents and trashed=false"}).GetList() 
    for file1 in file_list1:
     print('title: %s, id: %s' % (file1['title'],file1['id']))
     file1.GetContentFile(file1['title']) # 下載檔案     
     filepath = basepath+'/'+file1['title']
     pdfpath = basepath
     file_type = mimetypes.guess_type(file1['title'])[0]
     print(file_type)
     if file_type != 'application/pdf':
       doc2pdf_linux(filepath,pdfpath)
       name, suffix = os.path.splitext(file1['title']) 
       pdfname = name + '.pdf' 
     else:
       pdfname = file1['title']
     print("檔案列印中...")                 
     os.system("lp %s" % pdfname) # 檔案列印
     delete_gdrive(file1['id'], pdfname, file1['title'])    
  except:
    print("Downloading failed.")
    
def doc2pdf_linux(docPath, pdfPath):
    """
    允许的文档格式：doc，docx
    仅在linux平台下可以
    需要在linux中下载好libreoffice
    """
    #  注意cmd中的 libreoffice 要和 linux 中安装的一致
    # libreoffice 轉檔指令
    cmd = 'libreoffice --headless --convert-to pdf'.split() + [docPath] + ['--outdir'] + [pdfPath]    
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait(timeout=30)  # 停顿30秒等待转化
    stdout, stderr = p.communicate()  
    
def delete_gdrive(file_id, pdfname, filename):
  print(pdfname,filename)
  print("刪除文件檔...")
  #刪除 gdrive 文件檔案  
  gauth = GoogleAuth()
  #gauth.CommandLineAuth() #透過授權碼認證
  drive = GoogleDrive(gauth)
  file1 = drive.CreateFile({'id': file_id})
  file1.Delete()  
  #刪除本地端文件檔
  if pdfname == filename:
    os.remove(pdfname)
  else:
    os.remove(pdfname) 
    os.remove(filename)  
  
# paho callbacks
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc)) 
  client.subscribe("cups/cups0001", qos=1) # 用戶訂閱主題
  
def on_message(client, userdata, msg): # 收到訂閱訊息的處理    
    print(msg.topic + " " + msg.payload.decode())       
    if msg.payload.decode() == 'print':       
      download_gdrive_print()      
      
def initial():
  os.system("sh ngrok_url_linenotify.sh") 
  os.system("sh get_config.sh") 
  # 寫入 firebase realtimebase  
  with open("config.json", 'r')as f:
   for line in f.readlines():
    data = json.loads(line)
    print(data)    
    cups_ref.set(data)
    
if __name__ == "__main__":
 initial()
 client = mqtt.Client()  
 client.on_connect = on_connect  
 client.on_message = on_message  
 client.connect("broker.mqttdashboard.com", 1883) 
 client.loop_forever()            
 app.run(debug=True, host='0.0.0.0', port=5000)          
