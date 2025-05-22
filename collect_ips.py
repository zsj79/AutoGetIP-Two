import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urlparse

# 目标URL列表
urls = [
    'https://api.uouin.com/cloudflare.html',
    'https://www.wetest.vip/page/cloudflare/address_v4.html',
    'https://ip.164746.xyz',
    'https://cf-ip.cdtools.click/chengdu',
    'https://cf-ip.cdtools.click/beijing',
    'https://cf-ip.cdtools.click/shanghai',
    'https://cf-ip.cdtools.click/shenzhen',
    'https://monitor.gacjie.cn/page/cloudflare/ipv4.html'
]

# 配置字典：域名 -> 对应的选择器
site_config = {
    #'ip.164746.xyz': {'selector': 'tr'},
    #'monitor.gacjie.cn': {'selector': 'tr'}
}

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

if os.path.exists('autoip.txt'):
    os.remove('autoip.txt')

with open('autoip.txt', 'w') as file:
    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # 检查HTTP错误
            
            soup = BeautifulSoup(response.text, 'html.parser')
            domain = urlparse(url).netloc  # 获取域名
            selector = site_config.get(domain, {}).get('selector', 'tr')  # 默认tr
            
            elements = soup.find_all(selector)
            ips = []
            for el in elements:
                text = el.get_text()
                found_ips = re.findall(ip_pattern, text)
                if found_ips:
                    ips.extend(found_ips)
            
            # 去重并写入
            if ips:
                unique_ips = list(set(ips))
                file.write('\n'.join(unique_ips) + '\n')
                print(f"成功从 {url} 提取到 {len(unique_ips)} 个IP。")
            else:
                print(f"警告：{url} 未找到IP。")
                
        except Exception as e:
            print(f"处理 {url} 时出错: {str(e)}")
            continue

print('IP地址已保存至autoip.txt。')
