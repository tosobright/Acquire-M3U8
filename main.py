# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 21:33:35 2024

@author: toso
"""

import requests
import json
import os
import time
import subprocess

keyword = '庆余年 第二季'
downloadDir = '庆余年'
index = -1
apiJsonUrl = 'https://jszyapi.com/api.php/provide/vod'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}

abspath = os.path.dirname(__file__)
ffmpegpath = os.path.join(abspath,"ffmpeg.exe")
print(abspath)
url = apiJsonUrl + '/?wd=' + keyword +'&pg=0&ac=videolist'
all_content = requests.get(url).text
data = json.loads(all_content)
totalpage = data['pagecount']
for i in range(totalpage):
    url = apiJsonUrl + '/?wd=' + keyword +'&pg=' + str(i+1) + '&ac=videolist'
    print(url)
    all_content = requests.get(url).text
    data = json.loads(all_content)
    for ls in data['list']:
        print(ls['vod_name'])
        folderPath = os.path.join(abspath + '\\' + downloadDir, ls['vod_name'])
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        res = requests.get(ls['vod_pic'], timeout=5, headers=headers)
        if res.status_code == 200:
            picpath = os.path.join(folderPath, 'pic.png')
            with open(picpath, 'ab') as f:
                f.write(res.content)
            time.sleep(1)
        m3u8zy = ls['vod_play_url'].split('$$$')
        for m3u8 in m3u8zy:
            if('m3u8' in m3u8):
                downloadUrl = m3u8.split('#')
                for idx,url in enumerate(downloadUrl):
                    if idx > index:
                        name = url.split('$')[0]
                        durl = url.split('$')[1]
                        
                        vodpath = os.path.join(folderPath, name + '.mp4')
                        if not os.path.exists(vodpath):
                            print(vodpath,durl)
                            #ffmpeg -i http://xxxxx/test.m3u8 -c copy test.mp4                
                            command = ffmpegpath + " -rw_timeout 10000000 -i " + "\"" + durl + "\"" + " -c copy -y -bsf:a aac_adtstoasc -movflags +faststart " + "\"" + vodpath + "\""
                            print(command)
                            p = subprocess.run(command)       
                            p.wait()         


    
    
