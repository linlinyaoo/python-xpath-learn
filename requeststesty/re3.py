import requests
from bs4 import BeautifulSoup

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

for jd_label in jd_labels:
    # 获取标题
    title = jd_label.find('h5')
    if title:
        print(title.get_text().strip())

    # 获取内容列表
    content_ti = jd_label.find_all('div', class_='jd-js-title')
    content_ct = jd_label.find_all('div', class_='jd-js-content')
    for title, content in zip(content_ti, content_ct):
        ti = title.get_text(strip=True)
        ct =content.get_text(strip=True)
        print('---------------', title.get_text(strip=True), '---------------')
        print('-', content.get_text(strip=True))

    with open('1.xlsl','w',encoding='utf-8') as fp :
        fp.write(ti,ct)
        print('完成')




