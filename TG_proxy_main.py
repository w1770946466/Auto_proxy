# coding=utf-8
import base64
import requests
import re
import time
import os


update_path = "./sub/"

#获取群组聊天中的HTTP链接
def get_channel_http(url):
    headers = {
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://t.me/s/wbnet',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
    }
    response = requests.post(url, headers=headers)
    #print(response.text)
    pattren = re.compile(r'"https+:[^\s]*"')
    url_lst = pattren.findall(response.text)
    return url_lst


#对bs64解密
def jiemi_base64(data):  # 解密base64
    # data= '''{'aa':'bb'}'''
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    return base64.b64decode(data).decode('ascii')
    #print(type(base64.b64decode(data)))
    #b"{'name':'kkk','age':22}"
    #<class 'bytes'>


#判读是否为订阅链接
def get_content(url_lst):
    new_list = []
    #对链接进行格式化
    for i in url_lst:
        result = i.replace("\\", "").replace('"', "")
        if result not in new_list:
            new_list.append(result)
    #print(new_list)
    print("共获得", len(new_list), "条链接")
    end_list_clash = []
    end_list_v2ray = []
    end_bas64 = []
    #获取单个订阅链接进行判断
    i = 1
    for o in new_list:
        res = requests.get(o)
        #判断是否为clash
        try:
            skuid = re.findall('proxies:', res.text)[0]
            if skuid == "proxies:":
                print(i,".这是个clash订阅", o)
                end_list_clash.append(o)
        except:
            #判断是否为v2
            try:
                peoxy = jiemi_base64(res.text)
                print(i,".这是个v2ray订阅", o)
                end_list_v2ray.append(o)
                end_bas64.append(peoxy)
            #均不是则非订阅链接
            except:
                print(i,".非订阅链接")
        i += 1
    if end_list_v2ray == [] or end_list_clash == []:
        #print("https://oss.v2rayse.com/proxies/data/2022-07-08/cvSBda.yaml")
        return "https://oss.v2rayse.com/proxies/data/2022-07-08/cvSBda.yaml"
    else:
        #print(end_list[-1])
        bas64 = ''.join(end_bas64).replace('\n', "")
        t = time.localtime()
        date = time.strftime('%y%m', t)
        date_day = time.strftime('%y%m%d', t)
        try:
            os.mkdir(f'{update_path}{date}')
        except FileExistsError:
            pass
        txt_dir = update_path + date + '/' + date_day + '.txt'
        file = open(txt_dir, 'w', encoding= 'utf-8')
        file.write(bas64)
        file.close()
        file_L = open("Long_term_subscription.txt", 'w', encoding= 'utf-8')
        file_L.write(bas64)
        file_L.close()
        return end_list_clash[-1],end_list_v2ray[-1]


if __name__ == '__main__':
    url = "https://t.me/s/kxswa"
    resp = get_content(get_channel_http(url))
    print(resp)
