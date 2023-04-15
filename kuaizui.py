import requests
import re

e_sub =[]

def get_kkzui():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
    res = requests.get("https://kkzui.com/jd?orderby=modified", headers=headers)
    article_url = re.search(
        r'<h2 class="item-heading"><a href="(https://kkzui.com/(.*?)\.html)"', res.text).groups()[0]
    print(article_url)
    res = requests.get(article_url, headers=headers)
    sub_url = re.search(
        r'<p><strong>这是v2订阅地址</strong>：(.*?)</p>', res.text).groups()[0]
    e_sub.append(sub_url)
    print("获取kkzui.com完成！")
        
get_kkzui()
