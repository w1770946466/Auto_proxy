# coding=utf-8
import base64
import requests
import re
import time
import os
import threading
from tqdm import tqdm
import random, string
import datetime
from time import sleep


#文件路径
update_path = "./sub/"
#所有的clash订阅链接
end_list_clash = []
#所有的v2ray订阅链接
end_list_v2ray = []
#所有的节点明文信息
end_bas64 = []
#获得格式化后的链接
new_list = []
#永久订阅
e_sub = ['https://raw.githubusercontent.com/freefq/free/master/v2','https://proxy.huwo.club/v2ray.txt','https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub','https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2','https://raw.githubusercontent.com/learnhard-cn/free_proxy_ss/main/free','https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub','https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2']
#e_sub = ['https://pastebin.com/raw/dmnL3uAR','https://openit.uitsrt.top/long','https://raw.githubusercontent.com/freefq/free/master/v2','https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub','https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2','https://raw.githubusercontent.com/kxswa/k/k/base64']
#频道
urls =["https://t.me/s/masco899","https://t.me/s/wxdy666","https://t.me/s/nice16688","https://t.me/s/airproxies","https://t.me/s/jokerbphome","https://t.me/s/kxswa","https://t.me/s/BaiPiao166","https://t.me/s/beiyiwangdeguodu","https://t.me/s/baipiaoi","https://t.me/s/helloworld_1024","https://t.me/s/dingyue_Center","https://t.me/s/fffffx2","https://t.me/s/xuanyizero"]
#线程池
threads = []
#机场链接
plane_sub = ['https://www.prop.cf/?name=paimon&client=base64']
#机场试用链接
try_sub = []
#获取频道订阅的个数
sub_n = -5

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
    response = requests.post(
        url, headers=headers)
    #print(response.text)
    pattren = re.compile(r'"https+:[^\s]*"')
    url_lst = pattren.findall(response.text)
    #print('获取到',len(url_lst),'个网址')
    #print(url_lst)
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
def get_content(url):
    #print('【获取频道',url,'】')
    url_lst = get_channel_http(url)
    #print(url_lst)
    #对链接进行格式化
    for i in url_lst:
        result = i.replace("\\", "").replace('"', "")
        if result not in new_list:
            if "t" not in result[8]:
                if "p" not in result[-2]:
                    new_list.append(result)
    #print(new_list)
    #print("共获得", len(new_list), "条链接")
    #获取单个订阅链接进行判断
    i = 1
    try:
        new_list_down = new_list[sub_n::]
    except:
        new_list_down = new_list[len(new_list) * 2 // 3::]
    #print("共获得", len(new_list_down), "条链接")
    #print('【判断链接是否为订阅链接】')
    for o in new_list_down:
        try:
            res = requests.get(o)
            #判断是否为clash
            try:
                skuid = re.findall('proxies:', res.text)[0]
                if skuid == "proxies:":
                    #print(i, ".这是个clash订阅", o)
                    end_list_clash.append(o)
            except:
                #判断是否为v2
                try:
                    #解密base64
                    peoxy = jiemi_base64(res.text)
                    #print(i, ".这是个v2ray订阅", o)
                    end_list_v2ray.append(o)
                    end_bas64.extend(peoxy.splitlines())
                    
                #均不是则非订阅链接
                except:
                    #print(i, ".非订阅链接")
                    pass
        except:
            #print("第", i, "个链接获取失败跳过！")
            pass
        i += 1
    return end_bas64


def write_document():
    if end_list_v2ray == [] or end_list_clash == []:
        #print("https://oss.v2rayse.com/proxies/data/2022-07-08/cvSBda.yaml")
        return "https://oss.v2rayse.com/proxies/data/2022-07-08/cvSBda.yaml"
    else:
        #永久订阅
        em = 1
        for e in e_sub:
            try:
                res = requests.get(e)
                proxys=jiemi_base64(res.text)
                end_bas64.extend(proxys.splitlines())
            except:
                print("第",em,"永久订阅出现错误❌跳过")
            em += 1
        print('永久订阅更新完毕')
        
        #去重
        end_bas64_A = list(set(end_bas64))
        print("去重完毕！！去除",len(end_bas64) - len(end_bas64_A),"个重复节点")
        bas64 = '\n'.join(end_bas64_A).replace('\n\n', "\n").replace('\n\n', "\n").replace('\n\n', "\n")
        
        #获取时间，给文档命名用
        t = time.localtime()
        date = time.strftime('%y%m', t)
        date_day = time.strftime('%y%m%d', t)
        #创建文件路径
        try:
            os.mkdir(f'{update_path}{date}')
        except FileExistsError:
            pass
        txt_dir = update_path + date + '/' + date_day + '.txt'
        #写入时间订阅
        file = open(txt_dir, 'w', encoding='utf-8')
        file.write(bas64)
        file.close()       
        
        #减少获取的个数
        r = 1
        length = len(end_bas64_A)  # 总长
        m = 8  # 切分成多少份
        step = int(length / m) + 1  # 每份的长度
        for i in range(0, length, step):
            print("起",i,"始",i+step)
            zhengli = '\n'.join(end_bas64_A[i: i + step]).replace('\n\n', "\n").replace('\n\n', "\n").replace('\n\n', "\n")
            #将获得的节点变成base64加密，为了长期订阅
            obj = base64.b64encode(zhengli.encode())
            plaintext_result = obj.decode()
            #写入长期订阅
            file_L = open("Long_term_subscription"+str(r), 'w', encoding='utf-8')
            file_L.write(plaintext_result)
            r += 1
        #写入总长期订阅
        obj = base64.b64encode(bas64.encode())
        plaintext_result = obj.decode()
        file_L = open("Long_term_subscription_num", 'w', encoding='utf-8')
        file_L.write(plaintext_result)
        #写入README
        with open("README.md", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            f.close()
        now_time = datetime.datetime.now()
        TimeDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for index in range(len(lines)):
            try:
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription_num`\n':
                    lines.pop(index+1)
                    lines.insert(index+1, f'`节点总数: {length}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription1`\n':
                    lines.pop(index+1)
                    lines.insert(index+1, f'`合并节点总数: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription2`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`合并节点总数: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription3`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`合并节点总数: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription4`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`合并节点总数: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription5`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`合并节点总数: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription6`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`合并节点总数: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription7`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`合并节点总数: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription8`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`合并节点总数: {length-step*7}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription3.yaml`\n': # 目标行内容
                    lines.pop(index+4)
                    lines.pop(index+4)
                    lines.insert(index+4, f'更新时间：`{TimeDate}`\n')
                    lines.insert(index+4, f'### 试用高速订阅数量: `{len(try_sub)}`\n')
                if lines[index] == '>Trial subscription：\n': # 目标行内容
                    lines.pop(index)
                    lines.pop(index)
                """
                if lines[index] == '## ✨Star count\n': # 目标行内容
                    n = 5
                    for TrySub in try_sub:
                        lines.insert(index-n, f'\n>试用订阅：\n`{TrySub}`\n')
                        n += 3
                """
            except:
                #print("写入READ出错")
                pass
        #写入试用订阅
        for index in range(len(lines)):
            try:
                if lines[index] == '## ✨Star count\n': # 目标行内容
                    n = 5
                    for TrySub in try_sub:
                        #lines.insert(index+n-1, f'\n>')
                        lines.insert(index-n, f'\n>试用订阅：\n`{TrySub}`\n')
                        n += 3
            except:
                print("写入试用出错")
        
        with open("README.md", 'w', encoding='utf-8') as f:
            data = ''.join(lines)
            f.write(data)
        print("合并完成✅")
        try:
            numbers =sum(1 for _ in open(txt_dir))
            print("共获取到",numbers,"节点")
        except:
            print("出现错误！")
        
    return

#获取clash订阅
def get_yaml():
    print("开始获取clsah订阅")
    urls = ["https://api.dler.io//sub?target=clash&url=https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription1&insert=false&config=https://raw.githubusercontent.com/w1770946466/fetchProxy/main/config/provider/rxconfig.ini&emoji=true","https://api.dler.io//sub?target=clash&url=https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription2&insert=false&config=https://raw.githubusercontent.com/w1770946466/fetchProxy/main/config/provider/rxconfig.ini&emoji=true", "https://api.dler.io//sub?target=clash&url=https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription3&insert=false&config=https://raw.githubusercontent.com/w1770946466/fetchProxy/main/config/provider/rxconfig.ini&emoji=true"]
    n = 1
    for i in urls:
        response = requests.get(i)
        #print(response.text)
        file_L = open("Long_term_subscription" + str(n) +".yaml", 'w', encoding='utf-8')
        file_L.write(response.text)
        file_L.close()
        n += 1
    print("clash订阅获取完成！")

#获取机场试用订阅
def get_sub_url():
    V2B_REG_REL_URL = '/api/v1/passport/auth/register'
    # V2B_SUB_REL_URL = '/api/v1/user/getSubscribe'
    home_urls = (
        #'https://www.yifei999.com',
        #'https://www.funkyun.xyz'
        #'https://console.ly520.me',
        'https://www.ckcloud.xyz',
        'https://fastestcloud.xyz',
        'https://www.ckcloud.xyz',
        'https://fastestcloud.xyz',
        'https://shan-cloud.xyz',
        'http://hneko.xyz',
        'https://www.ckcloud.xyz',
        'https://user.bafang.vip',
        'https://cloud.hhygj.xyz',
        'https://feiniaoyun.top',
        'https://fastestcloud.xyz',
        'https://www.dgycom.com',
    )
    times = 1
    for current_url in home_urls:
        i = 0
        while i < times:
            header = {
                'Referer': current_url,
                'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            form_data = {
                'email': ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(12))+'@gmail.com',
                'password': 'autosub_v2b',
                'invite_code': '',
                'email_code': ''
            }
            #try:
                #print(current_url)
                #response = requests.post(current_url+V2B_REG_REL_URL, data=form_data,headers=header)
            #except:
                #print("获取订阅失败")
            '''
            if current_url == 'https://meal.leftright.buzz':
                try:
                    #print(current_url)
                    fan_res = requests.post('https://meal.leftright.buzz/api/v1/passport/auth/login', data=form_data,headers=header)
                    print(fan_res.text)
                    sleep(3)
                    auth_data = fan_res.json()["data"]["auth_data"]
                    print(auth_data)
                    fan_header = {
                        'Host': 'meal.leftright.buzz',
                        'Origin': 'https://meal.leftright.buzz',
                        'Authorization': ''.join(auth_data),
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Connection': 'keep-alive',
                        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
                        'Referer': 'https://meal.leftright.buzz/',
                    }
                    fan_data = {
                        'period': 'quarter_price',
                        'plan_id': '1',
                    }
                    fan_res_n = requests.post('https://meal.leftright.buzz/api/v1/user/order/save', headers=fan_header, data=fan_data)
                    print(fan_res_n.json()["data"])
                    fan_data_n = {
                        'trade_no':fan_res_n.json()["data"],
                        'method': '1',
                    }
                    fan_res_pay = requests.post('https://meal.leftright.buzz/api/v1/user/order/checkout', data=fan_data_n,headers=fan_header)
                    print("获取饭小溪订阅成功。。。",fan_res_pay.text)
                
                except Exception as result:
                    print(result)
                    break
            '''
            try:
                response = requests.post(current_url+V2B_REG_REL_URL, data=form_data,headers=header)
                subscription_url = f'{current_url}/api/v1/client/subscribe?token={response.json()["data"]["token"]}'
                e_sub.append(subscription_url)
                try_sub.append(subscription_url)
                #print(subscription_url)
                print("add:"+subscription_url)
            except:
                print("获取订阅失败")
            i += 1
            #print(f'Number succeeded: {i}\t{subscription_url}')

            
  
def get_kkzui():
    # ========== 抓取 kkzui.com 的节点 ==========
    try:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
        res = requests.get("https://kkzui.com/jd?orderby=modified",headers=headers)
        article_url = re.search(r'<h2 class="item-heading"><a href="(https://kkzui.com/(.*?)\.html)">20(.*?)号(.*?)个高速免费节点(.*?)免费代理</a></h2>',res.text).groups()[0]
        #print(article_url)
        res = requests.get(article_url,headers=headers)
        sub_url = re.search(r'<p><strong>这是v2订阅地址</strong>：(.*?)</p>',res.text).groups()[0]
        e_sub.append(sub_url)
    except:
        print("获取kkzui.com失败！")
    try:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
        res = requests.get("https://www.cfmem.com/search/label/free",headers=headers)
        article_url = re.search(r"https?://www\.cfmem\.com/\d{4}/\d{2}/\S+v2rayclash-vpn.html",res.text).group()
        #print(article_url)
        res = requests.get(article_url,headers=headers)
        sub_url = re.search(r'<span style="font-size: 15px;">(.*?)</span></span></div>',res.text).groups()[0]
        #print(sub_url)
        e_sub.append(sub_url)
    except Exception as e:
        print(e)
        
    
if __name__ == '__main__':
    print("========== 开始获取机场订阅链接 ==========")
    get_sub_url()
    print("========== 开始获取kkzui.com订阅链接 ==========")
    get_kkzui()
    print("========== 开始获取频道订阅链接 ==========")
    for url in urls:
        #print(url, "开始获取......")
        thread = threading.Thread(target=get_content,args = (url,))
        thread.start()
        threads.append(thread)
        #resp = get_content(get_channel_http(url))
        #print(url, "获取完毕！！")
    #等待线程结束
    for t in tqdm(threads):
        t.join()
    print("========== 准备写入订阅 ==========")
    res = write_document()
    clash_sub = get_yaml()
    print("========== 写入完成任务结束 ==========")
