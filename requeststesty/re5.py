import requests
from bs4 import BeautifulSoup
import re

url = "https://en.wikipedia.org/wiki/Soviet_Red_Army_Monument,_Harbin"

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
headers = {'User-Agent': user_agent}  # 更好的做法是将User-Agent放入headers中

response = requests.get(url, headers=headers)
response.raise_for_status()  # 检查请求是否成功


# 使用正则表达式去除HTML中的角标
pattern = r'\[\d+\]'
cleaned_html = re.sub(pattern, '', response.text)

# 将处理后的HTML传递给BeautifulSoup
soup = BeautifulSoup(cleaned_html, "html.parser")

su = soup.find(id="mw-content-text").find(class_=["mw-content-ltr", "mw-parser-output"])


# 遍历su中的所有<p>标签
for p in su.find_all("p"):
    # 使用正则表达式去除文本中的角标
    cleaned_text = re.sub(r'\[\d+\]', '', p.get_text(strip=True))
    print(cleaned_text)  # 打印清理后的文本