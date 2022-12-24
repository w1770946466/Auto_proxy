import requests
import yaml
import base64

# base64 编码的 v2ray 配置文件
# 获取 v2ray 订阅链接的内容
response = requests.get("https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/sub/2212/221224.txt")
encoded_v2ray_config = response.text
#encoded_v2ray_config = "eyJ2MiI6IHsiYWRkcmVzcyI6ICIxMjcuMC4wLjEiLCAicG9ydCI6IDQ0MywgInB1YmxpY0tleSI6ICI5NzE5NjJmMTYyNzM0ZTA5YjJlMzY5YTgxNzE1MmM5N2NhYjZkN2ZmMmQ2N2JjZTcyMmJkNzBhYjI4YzZjOWM1YjkiLCAidHlwZSI6ICJub25lIn19"

# 将 base64 编码的 v2ray 配置文件解码为原始字节
decoded_bytes = base64.b64decode(encoded_v2ray_config)

# 将原始字节转换为字符串
decoded_str = decoded_bytes.decode()

# 使用字符串格式化将 v2ray 配置转换为 clash 配置
clash_config = """
proxy-providers:
  - {name: "v2ray", type: vmess, server: "vmess://{}"}
""".format(decoded_str)

print(clash_config)

# 使用 pyyaml 库将内容解析成 Python 对象
v2ray_configs = yaml.safe_load(v2ray_configs)
print(v2ray_configs)
# 创建一个空的 clash 订阅列表
clash_configs = []

# 遍历 v2ray 配置列表
for config in v2ray_configs:
    # 将每个 v2ray 配置转换为 clash 配置
    clash_config = {
        "name": config["name"],
        "type": "vmess",
        "server": config["add"],
        "port": config["port"],
        "uuid": config["id"],
        "alterId": config["aid"],
        "cipher": config["security"],
        "network": config["net"],
        "ws-path": config["path"],
        "ws-headers": {
            "Host": config["host"],
        },
    }
    # 将转换后的 clash 配置添加到列表中
    clash_configs.append(clash_config)

# 将 clash 配置列表转换为 YAML 格式的字符串
clash_configs_yaml = yaml.dump(clash_configs)
print(clash_configs_yaml)
# 将字符串写入文件
#with open("clash_configs.yml", "w") as f:
    #f.write(clash_configs_yaml)
