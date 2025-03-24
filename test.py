import requests
import json
from pprint import pprint
import re
from demo import identify_word
import html
import csv

csv_file=open('movie.csv','w',encoding='utf-8',newline='')
csv_writer=csv.DictWriter(csv_file,fieldnames=['电影名称','上映时间','票房','场均人次','上座率','排片率','场次','票房数'])
csv_writer.writeheader()
def changer(Mapword,word):
    new_word=''
    for i in word:
        try:
            num=Mapword[ord(i)]
            new_word+=str(num)
        except:
            new_word+=i
    return new_word
'''
header={
    'cookie':'_lxsdk_cuid=195a6acb293c8-0e86746cc07f55-4c657b58-13c680-195a6acb294c8; _lxsdk=195a6acb293c8-0e86746cc07f55-4c657b58-13c680-195a6acb294c8; uuid=195a6acb293c8-0e86746cc07f55-4c657b58-13c680-195a6acb294c8; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; _lxsdk_s=195c807aeeb-12b-d51-9d5%7C%7C22',
    'host':'piaofang.maoyan.com',
    'referer':'https://piaofang.maoyan.com/dashboard/movie?date=2025-01-29',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
}

url='https://piaofang.maoyan.com/dashboard-ajax/movie?showDate=20250129&orderType=0&uuid=195a6acb293c8-0e86746cc07f55-4c657b58-13c680-195a6acb294c8&timeStamp=1742821386641&User-Agent=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzNC4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMzQuMC4wLjA%3D&index=435&channelId=40009&sVersion=2&signKey=461952371b32aebcfdde7bad046d00d5&WuKongReady=h5'

response=requests.get(url=url,headers=header)

text=response.text

with open('info.txt','w',encoding='utf-8') as f:
    f.write(text)
'''
text=open('info.txt','r',encoding='utf-8').read()
json_data=json.loads(text)


fontStyle=json_data['fontStyle']
font_url='https:'+re.findall(r'url\("(.*?)"\)',fontStyle)[-1]
font_text=requests.get(font_url).content
with open('font.woff','wb') as f:
    f.write(font_text)

map_word=identify_word('font.woff')



moveList=json_data['movieList']['list']
for index in moveList:
    movieName=index['movieInfo']['movieName']#电影名称
    releaseInfo=index['movieInfo']['releaseInfo']#上映时间
    boxRate=index['boxRate']#票房   
    avgShowView=index['avgShowView']#场均人次
    avgSeatView=index['avgSeatView']#上座率
    showCountRate=index['showCountRate']#排片率
    sumBoxDesc=index['sumBoxDesc']#累计票房
    showCount=index['showCount']#场次
    boxSplitUnit=index['boxSplitUnit']['num']#票房单位
    d_word=html.unescape(boxSplitUnit)
    new_num=changer(map_word,d_word)
    dit={'电影名称':movieName,
         '上映时间':releaseInfo,
         '票房':sumBoxDesc,
         '场均人次':avgShowView,
         '上座率':avgSeatView,
         '排片率':showCountRate,
         '场次':showCount,
         '票房数':new_num
         }
    csv_writer.writerow(dit)

