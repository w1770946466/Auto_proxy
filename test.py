import requests
import yaml

# 获取 v2ray 订阅链接的内容
response = requests.get("https://your-v2ray-subscription-link.com")
v2ray_configs = response.text

# 使用 pyyaml 库将内容解析成 Python 对象
v2ray_configs = yaml.safe_load(v2ray_configs)

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

# 将字符串写入文件
with open("clash_configs.yml", "w") as f:
    f.write(clash_configs_yaml)
