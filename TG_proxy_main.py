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
import chardet

#试用机场链接
home_urls = (
    'https://xn--30rs3bu7r87f.com',
    'https://seeworld.pro',          #5T   永久
    'https://fastestcloud.xyz',      #2G   1天
    'https://www.ckcloud.xyz',       #1G   1天
)
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
e_sub = ['https://sub.pmsub.me/base64','https://www.prop.cf/?name=paimon&client=base64','https://raw.githubusercontent.com/yaney01/Yaney01/main/temporary','https://sub.pmsub.me/base64','https://raw.githubusercontent.com/hkaa0/permalink/main/proxy/V2ray','https://sub.sharecentre.online/sub','https://raw.githubusercontent.com/freefq/free/master/v2','https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub','https://raw.githubusercontent.com/learnhard-cn/free_proxy_ss/main/free','https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub']
#e_sub = ['https://pastebin.com/raw/dmnL3uAR','https://openit.uitsrt.top/long','https://raw.githubusercontent.com/freefq/free/master/v2','https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub','https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2','https://raw.githubusercontent.com/kxswa/k/k/base64']
#频道
urls =["https://t.me/s/freeVPNjd","https://t.me/s/wxdy666","https://t.me/s/nice16688","https://t.me/s/go4sharing","https://t.me/s/helloworld_1024","https://t.me/s/dingyue_Center","https://t.me/s/ZDYZ2"]
#线程池
threads = []
#机场链接
plane_sub = ['https://www.prop.cf/?name=paimon&client=base64']
#机场试用链接
try_sub = []
#获取频道订阅的个数
sub_n = -5
#试用节点明文
end_try = []

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
    # 对 Base64 编码后的字符串进行解码，得到字节字符串
    decoded_bytes = base64.b64decode(data)
    # 使用 chardet 库自动检测字节字符串的编码格式
    encoding = chardet.detect(decoded_bytes)['encoding']
    # 将字节字符串转换为字符串
    decoded_str = decoded_bytes.decode(encoding)
    return decoded_str

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

#写入文件
def write_document():
    if e_sub == [] or try_sub == []:
        print("订阅为空请检查！")
    else:
        #永久订阅
        random.shuffle(e_sub)
        for e in e_sub:
            try:
                res = requests.get(e)
                proxys=jiemi_base64(res.text)
                end_bas64.extend(proxys.splitlines())
            except:
                print(e,"永久订阅出现错误❌跳过")
        print('永久订阅更新完毕')
        #试用订阅
        random.shuffle(try_sub)
        for t in try_sub:
            try:
                res = requests.get(t)
                proxys=jiemi_base64(res.text)
                end_try.extend(proxys.splitlines())
            except Exception as er:
                print(t,"试用订阅出现错误❌跳过",er)
        print('试用订阅更新完毕',try_sub)
        #永久订阅去重
        end_bas64_A = list(set(end_bas64))
        print("去重完毕！！去除",len(end_bas64) - len(end_bas64_A),"个重复节点")
        #永久订阅去除多余换行符
        bas64 = '\n'.join(end_bas64_A).replace('\n\n', "\n").replace('\n\n', "\n").replace('\n\n', "\n")
        #试用去除多余换行符
        bas64_try = '\n'.join(end_try).replace('\n\n', "\n").replace('\n\n', "\n").replace('\n\n', "\n")
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
        #写入试用订阅
        obj_try = base64.b64encode(bas64_try.encode())
        plaintext_result_try = obj_try.decode()
        file_L_try = open("Long_term_subscription_try", 'w', encoding='utf-8')
        file_L_try.write(plaintext_result_try)
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
                    lines.insert(index+1, f'`Total number of merge nodes: {length}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription1`\n':
                    lines.pop(index+1)
                    lines.insert(index+1, f'`Total number of merge nodes: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription2`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`Total number of merge nodes: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription3`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`Total number of merge nodes: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription4`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`Total number of merge nodes: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription5`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`Total number of merge nodes: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription6`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`Total number of merge nodes: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription7`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`Total number of merge nodes: {step}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription8`\n': # 目标行内容
                    lines.pop(index+1)
                    lines.insert(index+1, f'`Total number of merge nodes: {length-step*7}`\n')
                if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription3.yaml`\n': # 目标行内容
                    lines.pop(index+4)
                    lines.pop(index+4)
                    lines.insert(index+4, f'Updata：`{TimeDate}`\n')
                    lines.insert(index+4, f'### Try the number of high-speed subscriptions: `{len(try_sub)}`\n')
                if lines[index] == '>Trial subscription：\n': # 目标行内容
                    lines.pop(index)
                    lines.pop(index)
                """
                if lines[index] == '## ✨Star count\n': # 目标行内容
                    n = 5
                    for TrySub in try_sub:
                        lines.insert(index-n, f'\n>Trial subscription：\n`{TrySub}`\n')
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
                        lines.insert(index-n, f'\n>Trial subscription：\n`{TrySub}`\n')
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
    urls = ["https://api.dler.io//sub?target=clash&url=https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription_try&insert=false&config=https://raw.githubusercontent.com/w1770946466/fetchProxy/main/config/provider/rxconfig.ini&emoji=true","https://api.dler.io//sub?target=clash&url=https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription2&insert=false&config=https://raw.githubusercontent.com/w1770946466/fetchProxy/main/config/provider/rxconfig.ini&emoji=true", "https://api.dler.io//sub?target=clash&url=https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription3&insert=false&config=https://raw.githubusercontent.com/w1770946466/fetchProxy/main/config/provider/rxconfig.ini&emoji=true"]
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
            if current_url == 'https://xn--4gqu8thxjfje.com' or current_url == 'https://seeworld.pro'  or current_url == 'https://www.jwckk.top'or current_url == 'https://vvtestatiantian.top':
                try:
                    fan_res = requests.post(
                        f'{current_url}/api/v1/passport/auth/register', data=form_data, headers=header)
                    auth_data = fan_res.json()["data"]["auth_data"]
                    #print(auth_data)
                    fan_header = {
                        'Origin': current_url,
                        'Authorization': ''.join(auth_data),
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Connection': 'keep-alive',
                        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
                        'Referer': current_url,
                    }
                    fan_data = {
                        'period': 'onetime_price',
                        'plan_id': '1',
                    }
                    fan_res_n = requests.post(
                        f'{current_url}/api/v1/user/order/save', headers=fan_header, data=fan_data)
                    #print(fan_res_n.json()["data"])
                    fan_data_n = {
                        'trade_no':fan_res_n.json()["data"],
                        #'method': '1',
                    }
                    fan_res_pay = requests.post(
                        f'{current_url}/api/v1/user/order/checkout', data=fan_data_n, headers=fan_header)
                    subscription_url = f'{current_url}/api/v1/client/subscribe?token={fan_res.json()["data"]["token"]}'
                    try_sub.append(subscription_url)
                    #e_sub.append(subscription_url)
                    print("add:"+subscription_url)
                except Exception as result:
                    print(result)
                    break
            else:
                try:
                    response = requests.post(
                        current_url+V2B_REG_REL_URL, data=form_data, headers=header)
                    subscription_url = f'{current_url}/api/v1/client/subscribe?token={response.json()["data"]["token"]}'
                    try_sub.append(subscription_url)
                    #e_sub.append(subscription_url)
                    print("add:"+subscription_url)
                except Exception as e:
                    print("获取订阅失败",e)
            i += 1

            
 # ========== 抓取 kkzui.com 的节点 ==========  
def get_kkzui():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
        res = requests.get("https://kkzui.com/jd?orderby=modified", headers=headers)
        article_url = re.search(r'class="media-content" href="(.*?)"', res.text).groups()[0]
        #print(article_url)
        res = requests.get(article_url, headers=headers)
        sub_url = re.search(
            r'<strong>这是v2订阅地址：(.*?)</strong>', res.text).groups()[0]
        #print(sub_url)
        try_sub.append(sub_url)
        e_sub.append(sub_url)
        print("获取kkzui.com完成！")
    except Exception as e:
        print(e)
        print("获取kkzui.com失败！")
        
# ========== 抓取 cfmem.com 的节点 ==========
def get_cfmem():
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
        print("获取cfmem.com完成！")
    except Exception as e:
        print(e)
        print("获取cfmem.com失败！")

# ========== 抓取 v2rayshare.com 的节点 ==========
def get_v2rayshare():
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
        #print(sub_url)
        try_sub.append(sub_url)
        e_sub.append(sub_url)
        print("获取v2rayshare.com完成！")
    except Exception as e:
        print("获取v2rayshare.com失败！",e)

# ========== 抓取 nodefree.org 的节点 ==========
def get_nodefree():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
        res = requests.get(
            "https://nodefree.org/", headers=headers)
        #print(res.text)
        article_url = re.search(
            r'https://nodefree.org/p/\d+\.html', res.text).group()
        #print(article_url)
        res = requests.get(article_url, headers=headers)
        sub_url = re.search(
            r'<p>https://nodefree.org/dy/(.*?)</p>', res.text).groups()[0]
        sub_url = 'https://nodefree.org/dy/'+sub_url
        #print(sub_url)
        try_sub.append(sub_url)
        e_sub.append(sub_url)
        print("获取nodefree.org完成！")
    except Exception as e:
        print("获取nodefree.org失败！",e)
        
    
if __name__ == '__main__':
    print("========== 开始获取机场订阅链接 ==========")
    get_sub_url()
    print("========== 开始获取网站订阅链接 ==========")
    get_kkzui()
    get_cfmem()
    get_v2rayshare()
    get_nodefree()
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
