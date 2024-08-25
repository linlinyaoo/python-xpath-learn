import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


url = 'http://www.atguigu.com/bigdata/'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'Accept-Language': 'zh-CN,zh;q=0.9',  # 设置接受的语言
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'text/html;Charset=utf-8'
}

response = requests.get(url=url, headers=headers)

# 使用字节数据并手动解码
content = response.content.decode('utf-8', errors='ignore')

# 使用 BeautifulSoup 解析解码后的内容
soup = BeautifulSoup(content, 'html.parser')

# 查找包含课程信息的 div 标签
course_info_div = soup.find('div', class_='jd-content')

# 查找所有的课程信息标签
jd_labels = course_info_div.find_all('div', class_='jd-label')

# 创建一个新的 Excel 工作簿
wb = Workbook()
ws = wb.active

# 设置 Excel 表头
ws.append(['标题', '内容'])

for jd_label in jd_labels:
    # 获取标题
    title = jd_label.find('h5')
    if title:
        title_text = title.get_text(strip=True)

    # 获取内容列表
    content_ti = jd_label.find_all('div', class_='jd-js-title')
    content_ct = jd_label.find_all('div', class_='jd-js-content')
    for ti, ct in zip(content_ti, content_ct):
        # 将标题和内容组合成一个字符串
        content_text = f'{ti.get_text(strip=True)} - {ct.get_text(strip=True)}'
        # 将标题和内容写入 Excel 文件
        ws.append([title_text, content_text])

# 保存 Excel 文件
wb.save('1.xlsx')
print('完成')
