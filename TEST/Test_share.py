import requests
import re


try_sub = []
e_sub = []

try:
      headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
      res = requests.get("https://www.cfmem.com/search/label/free",headers=headers)
      article_url = re.search(r"https?://www\.cfmem\.com/\d{4}/\d{2}/\S+v2rayclash-vpn.html",res.text).group()
      #print(article_url)
      res = requests.get(article_url,headers=headers)
      sub_url = re.search(r'>v2ray订阅链接&#65306;(.*?)</span>',res.text).groups()[0]
      #print(sub_url)
      try_sub.append(sub_url)
      e_sub.append(sub_url)
except Exception as e:
      print(e)
      print("获取cfmem.com失败！")
