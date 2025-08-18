import requests
import re
import os

# 目标URL列表
urls = [
    'https://www.wetest.vip/page/cloudflare/address_v4.html'
]

# 正则表达式用于匹配IP地址
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 使用列表存储IP地址以保持顺序，同时手动去重
ordered_unique_ips = []

for url in urls:
    try:
        # 发送HTTP请求获取网页内容
        response = requests.get(url, timeout=5)
        
        # 确保请求成功
        if response.status_code == 200:
            # 获取网页的文本内容
            html_content = response.text
            
            # 使用正则表达式查找所有IP地址
            ip_matches = re.findall(ip_pattern, html_content, re.IGNORECASE)
            
            # 遍历找到的IP，如果列表中没有，就添加进去，以保持顺序并去重
            for ip in ip_matches:
                if ip not in ordered_unique_ips:
                    ordered_unique_ips.append(ip)

    except requests.exceptions.RequestException as e:
        print(f'请求 {url} 失败: {e}')
        continue

# 将去重后且保持抓取顺序的IP地址写入文件
if ordered_unique_ips:
    with open('ip.txt', 'w') as file:
        for ip in ordered_unique_ips:
            file.write(ip + '\n')
    print(f'已按抓取顺序保存 {len(ordered_unique_ips)} 个唯一IP地址到ip.txt文件。')
else:
    print('未找到有效的IP地址。')
