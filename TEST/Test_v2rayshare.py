import requests
import re


try_sub = []
e_sub = []

try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
        res = requests.get(
            "https://v2rayshare.com/", headers=headers)
        #print(res.text)
        article_url = re.search(
            r'https://v2rayshare.com/p/\d+\.html', res.text).group()
        #print(article_url)
        res = requests.get(article_url, headers=headers)
        sub_url = re.search(
            r'<p>https://v2rayshare.com/wp-content/uploads/(.*?)</p>', res.text).groups()[0]
        sub_url = 'https://v2rayshare.com/wp-content/uploads/'+sub_url
        print(sub_url)
        try_sub.append(sub_url)
        e_sub.append(sub_url)
        print("获取v2rayshare.com成功！")
except Exception as e:
        print(e)
