# 说明 : 本脚本提供解析v2ray/ss/ssr/clashR/clashX订阅链接为Clash配置文件,仅供学习交流使用.
# https://github.com/Celeter/convert2clash
import os, re, sys, json, base64, datetime
import requests, yaml
import urllib.parse


#命名数字


def log(msg):
    time = datetime.datetime.now()
    print('[' + time.strftime('%Y.%m.%d-%H:%M:%S') + '] ' + msg)


# 保存到文件
def save_to_file(file_name, content):
    with open(file_name, 'wb') as f:
        f.write(content)


# 针对url的base64解码
def safe_decode(s):
    num = len(s) % 4
    if num:
        s += '=' * (4 - num)
    return base64.urlsafe_b64decode(s)


# 解析vmess节点
def decode_v2ray_node(nodes):
    proxy_list = []
    for node in nodes:
        decode_proxy = node.decode('utf-8')[8:]
        if not decode_proxy or decode_proxy.isspace():
            log('vmess节点信息为空，跳过该节点')
            continue
        proxy_str = base64.b64decode(decode_proxy).decode('utf-8')
        proxy_dict = json.loads(proxy_str)
        proxy_list.append(proxy_dict)
    #print(proxy_list)
    return proxy_list


# 解析ss节点
def decode_ss_node(nodes):
    proxy_list = []
    for node in nodes:
        decode_proxy = node.decode('utf-8')[5:]
        if not decode_proxy or decode_proxy.isspace():
            log('ss节点信息为空，跳过该节点')
            continue
        info = dict()
        param = decode_proxy
        if param.find('#') > -1:
            remark = urllib.parse.unquote(param[param.find('#') + 1:])
            info['name'] = remark
            param = param[:param.find('#')]
        if param.find('/?') > -1:
            plugin = urllib.parse.unquote(param[param.find('/?') + 2:])
            param = param[:param.find('/?')]
            for p in plugin.split(';'):
                key_value = p.split('=')
                info[key_value[0]] = key_value[1]
        if param.find('@') > -1:
            matcher = re.match(r'(.*?)@(.*):(.*)', param)
            if matcher:
                param = matcher.group(1)
                info['server'] = matcher.group(2)
                info['port'] = matcher.group(3)
            else:
                continue
            matcher = re.match(r'(.*?):(.*)', safe_decode(param).decode('utf-8'))
            if matcher:
                info['method'] = matcher.group(1)
                info['password'] = matcher.group(2)
            else:
                continue
        else:
            matcher = re.match(r'(.*?):(.*)@(.*):(.*)', safe_decode(param).decode('utf-8'))
            if matcher:
                info['method'] = matcher.group(1)
                info['password'] = matcher.group(2)
                info['server'] = matcher.group(3)
                info['port'] = matcher.group(4)
            else:
                continue
        proxy_list.append(info)
    #print(proxy_list)
    return proxy_list


# 解析ssr节点
def decode_ssr_node(nodes):
    proxy_list = []
    for node in nodes:
        decode_proxy = node.decode('utf-8')[6:]
        if not decode_proxy or decode_proxy.isspace():
            log('ssr节点信息为空，跳过该节点')
            continue
        proxy_str = safe_decode(decode_proxy).decode('utf-8')
        parts = proxy_str.split(':')
        if len(parts) != 6:
            print('该ssr节点解析失败，链接:{}'.format(node))
            continue
        info = {
            'server': parts[0],
            'port': parts[1],
            'protocol': parts[2],
            'method': parts[3],
            'obfs': parts[4]
        }
        password_params = parts[5].split('/?')
        info['password'] = safe_decode(password_params[0]).decode('utf-8')
        params = password_params[1].split('&')
        for p in params:
            key_value = p.split('=')
            info[key_value[0]] = safe_decode(key_value[1]).decode('utf-8')
        proxy_list.append(info)
    return proxy_list


# 获取订阅地址数据:
def get_proxies(urls):
    url_list = urls.split(';')
    headers = {
        'User-Agent': 'Rule2Clash'
    }
    proxy_list = {
        'proxy_list': [],
        'proxy_names': []
    }
    # 请求订阅地址
    for url in url_list:
        response = requests.get(url, headers=headers, timeout=5000).text
        try:
            raw = base64.b64decode(response)
        except Exception as r:
            log('base64解码失败:{},应当为clash节点'.format(r))
            log('clash节点提取中...')
            yml = yaml.load(response, Loader=yaml.FullLoader)
            nodes_list = []
            tmp_list = []
            # clash新字段
            if yml.get('proxies'):
                tmp_list = yml.get('proxies')
            # clash旧字段
            elif yml.get('Proxy'):
                tmp_list = yml.get('Proxy')
            else:
                log('clash节点提取失败,clash节点为空')
                continue
            for node in tmp_list:
                node['name'] = node['name'].strip() if node.get('name') else None
                # 对clashR的支持
                if node.get('protocolparam'):
                    node['protocol-param'] = node['protocolparam']
                    del node['protocolparam']
                if node.get('obfsparam'):
                    node['obfs-param'] = node['obfsparam']
                    del node['obfsparam']
                node['udp'] = True
                nodes_list.append(node)
            node_names = [node.get('name') for node in nodes_list]
            log('可用clash节点{}个'.format(len(node_names)))
            proxy_list['proxy_list'].extend(nodes_list)
            proxy_list['proxy_names'].extend(node_names)
            continue
        nodes_list = raw.splitlines()
        clash_node = []
        for node in nodes_list:
            try:
                if node.startswith(b'vmess://'):
                    decode_proxy = decode_v2ray_node([node])
                    clash_node = v2ray_to_clash(decode_proxy)
                elif node.startswith(b'ss://'):
                    decode_proxy = decode_ss_node([node])
                    clash_node = ss_to_clash(decode_proxy)
                elif node.startswith(b'ssr://'):
                    decode_proxy = decode_ssr_node([node])
                    clash_node = ssr_to_clash(decode_proxy)
                else:
                    pass
                proxy_list['proxy_list'].extend(clash_node['proxy_list'])
                proxy_list['proxy_names'].extend(clash_node['proxy_names'])
            except Exception as e:
                print(f'出错{e}')
                
    log('共发现:{}个节点'.format(len(proxy_list['proxy_names'])))
    #print(proxy_list)
    return proxy_list


# v2ray转换成Clash节点
def v2ray_to_clash(arr):
    log('v2ray节点转换中...')
    proxies = {
        'proxy_list': [],
        'proxy_names': []
    }
    num = 0
    for item in arr:
        num += 1
        if item.get('ps') is None and item.get('add') is None and item.get('port') is None \
                and item.get('id') is None and item.get('aid') is None:
            continue
        obj = {
            'name': item.get('ps').strip() if item.get('ps') else None,
            #'name': f"Auto_proxy{num}",
            'type': 'vmess',
            'server': item.get('add'),
            'port': int(item.get('port')),
            'uuid': item.get('id'),
            'alterId': item.get('aid'),
            'cipher': 'auto',
            'udp': True,
            # 'network': item['net'] if item['net'] and item['net'] != 'tcp' else None,
            'network': item.get('net'),
            'tls': True if item.get('tls') == 'tls' else None,
            'ws-path': item.get('path'),
            'ws-headers': {'Host': item.get('host')} if item.get('host') else None
        }
        for key in list(obj.keys()):
            if obj.get(key) is None:
                del obj[key]
        #'''
        if obj.get('alterId') is not None:
            try:
                proxies['proxy_list'].append(obj)
                proxies['proxy_names'].append(obj['name'])
            except:
                print('id获取失败')
         #'''
    #print(proxies)
    log('可用v2ray节点{}个'.format(len(proxies['proxy_names'])))
    return proxies


# ss转换成Clash节点
def ss_to_clash(arr):
    log('ss节点转换中...')
    proxies = {
        'proxy_list': [],
        'proxy_names': []
    }
    for item in arr:
        obj = {
            'name': item.get('name').strip() if item.get('name') else None,
            'type': 'ss',
            'server': item.get('server'),
            'port': int(item.get('port')),
            'cipher': item.get('method'),
            'password': item.get('password'),
            'plugin': 'obfs' if item.get('plugin') and item.get('plugin').startswith('obfs') else None,
            'plugin-opts': {} if item.get('plugin') else None
        }
        if item.get('obfs'):
            obj['plugin-opts']['mode'] = item.get('obfs')
        if item.get('obfs-host'):
            obj['plugin-opts']['host'] = item.get('obfs-host')
        for key in list(obj.keys()):
            if obj.get(key) is None:
                del obj[key]
        try:
            proxies['proxy_list'].append(obj)
            proxies['proxy_names'].append(obj['name'])
        except:
            print("ss转换失败！！")
            pass
    log('可用ss节点{}个'.format(len(proxies['proxy_names'])))
    #print(proxies)
    return proxies


# ssr转换成Clash节点
def ssr_to_clash(arr):
    log('ssr节点转换中...')
    proxies = {
        'proxy_list': [],
        'proxy_names': []
    }
    for item in arr:
        obj = {
            'name': item.get('remarks').strip() if item.get('remarks') else None,
            'type': 'ssr',
            'server': item.get('server'),
            'port': int(item.get('port')),
            'cipher': item.get('method'),
            'password': item.get('password'),
            'obfs': item.get('obfs'),
            'protocol': item.get('protocol'),
            'obfs-param': item.get('obfsparam'),
            'protocol-param': item.get('protoparam'),
            'udp': True
        }
        for key in list(obj.keys()):
            if obj.get(key) is None:
                del obj[key]
        if obj.get('name'):
            if not obj['name'].startswith('剩余流量') and not obj['name'].startswith('过期时间'):
                proxies['proxy_list'].append(obj)
                proxies['proxy_names'].append(obj['name'])
    log('可用ssr节点{}个'.format(len(proxies['proxy_names'])))
    return proxies


# 获取本地规则策略的配置文件
def load_local_config(path):
    try:
        f = open(path, 'r', encoding="utf-8")
        local_config = yaml.load(f.read(), Loader=yaml.FullLoader)
        f.close()
        return local_config
    except FileNotFoundError:
        log('配置文件加载失败')
        sys.exit()


# 获取规则策略的配置文件
def get_default_config(url, path):
    try:
        raw = requests.get(url, timeout=5000).content.decode('utf-8')
        template_config = yaml.load(raw, Loader=yaml.FullLoader)
    except requests.exceptions.RequestException:
        log('网络获取规则配置失败,加载本地配置文件')
        template_config = load_local_config(path)
    log('已获取规则配置文件')
    return template_config


# 将代理添加到配置文件
def add_proxies_to_model(data, model):
    
    #print(data['proxy_list'])
    #print(model)
    if data is None or model is None:
        raise ValueError('Invalid input: data and model cannot be None')
    if 'proxy_list' not in data or 'proxy_names' not in data:
        raise ValueError('Invalid input: data should contain "proxy_list" and "proxy_names" keys')
    
    try:
        if model.get('proxies') is None:
            model['proxies'] = data.get('proxy_list')
        else:
            model['proxies'].extend(data.get('proxy_list'))
    except Exception as e:
        print(f'Error adding proxies to model: {e}')

    try:
        #data['proxy_names'] = list(set(data['proxy_names']))
        data['proxy_list'] = [d for d in data['proxy_list'] if 'name' in d]
        names = []
        for item in data['proxy_list']:
            try:
                names.append(item['name'])
            except TypeError:
                # 处理 item 不是字典的情况
                print("Error: item is not a dictionary")
            except KeyError:
                # 处理字典中没有 name 字段的情况
                print("Error: dictionary does not have a 'name' field")
        #print(data['proxy_list'])
        for group in model.get('proxy-groups'):
            if group.get('proxies') is None:
                #group['proxies'] = data.get('proxy_names')
                group['proxies'] = names
            else:
                #group['proxies'].extend(data.get('proxy_names'))
                group['proxies'].extend(names)
    except Exception as e:
        print(f'Error adding proxy names to groups: {e}')

    return model






# 保存配置文件
def save_config(path, data):
    config = yaml.dump(data, sort_keys=False, default_flow_style=False, encoding='utf-8', allow_unicode=True)
    save_to_file(path, config)
    log('成功更新{}个节点'.format(len(data['proxies'])))


# 程序入口
if __name__ == '__main__':
    # 订阅地址 多个地址用;隔开
    #sub_url = input('请输入订阅地址(多个地址用;隔开):')
    sub_url = 'https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription2'
    # 输出路径
    output_path = './output.yaml'
    # 规则策略
    config_url = 'https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/config.yaml'
    config_path = './config.yaml'

    if sub_url is None or sub_url == '':
        sys.exit()
    node_list = get_proxies(sub_url)
    default_config = get_default_config(config_url, config_path)
    final_config = add_proxies_to_model(node_list, default_config)
    save_config(output_path, final_config)
    print(f'文件已导出至 {config_path}')
