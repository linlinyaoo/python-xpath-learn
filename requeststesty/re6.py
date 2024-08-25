import json
import re
from lxml import etree
import urllib
from bs4 import BeautifulSoup

def get_title(node):
    if node is None:
        return
    ori_data = node.xpath("//div[@class='el-col el-col-24']/h1[@class='name font-bold']/text()")
    title = ori_data[0]
    return title


def get_content(node):
    if node is None:
        return []

    # 使用XPath从当前节点开始搜索所有子节点
    ori_data = node.xpath(".//div[@class='long-container']//*")
    text = []
    current_h2 = None
    current_paragraph = []

    for p in ori_data:
        # 处理 <h2> 标签
        if p.tag == 'h2':
            # 如果当前有正在处理的段落，先将其添加到结果中
            if current_paragraph:
                text.append(f"{current_h2}:\n\t" + "\n\t".join(current_paragraph))
                # text.append(f"{current_h2}: {' '.join(current_paragraph)}")
                current_paragraph = []

            # 更新当前的 h2 标题
            current_h2 = p.text.strip() if p.text else ''

        # 处理 <p> 标签
        elif p.tag == 'p':
            paragraph_content = p.text.strip() if p.text else ''
            current_paragraph.append(paragraph_content)
            current_paragraph = [lst for lst in current_paragraph if lst]

        # 处理 <sub> 标签
        elif p.tag == 'sub':
            sub_html = etree.tostring(p, encoding='unicode', method='html').strip()
            if current_paragraph:
                current_paragraph[-1] += sub_html
            else:
                current_paragraph.append(sub_html)

    # 在循环结束后，检查是否还有未添加的段落
    if current_paragraph:
        text.append(f"{current_h2}:\n\t" + "\n\t".join(current_paragraph))
        # text.append(f"{current_h2}: {' '.join(current_paragraph)}")
    text = '\n'.join(text)
    return text

def get_app(node):
    if node is None:
        return None

    # 获取 long-container 内的所有子节点
    ori_data = node.xpath(".//div[@class='long-container']//*")
    text = []
    capturing = False  # 标记是否已找到执行标准的 h2 标签

    for p in ori_data:
        if p.tag == 'h2' and "执行标准" in p.text:
            capturing = True  # 找到 h2 标签后，开始捕获 p 标签内容
            continue  # 跳到下一个元素以查找 p 标签

        if capturing and p.tag == 'p' and p.text:
            c2 = p.text.strip()
            text.append(c2)  # 将提取的内容添加到列表中
            break  # 找到 p 标签后，结束循环
    text = ''.join(text)

    return text if text else None  # 返回结果或 None


def get_con(node):
    if node is None:
        return None

    # 获取 long-container 内的所有子节点
    ori_data = node.xpath(".//div[@class='long-container']//*")
    text = []
    capturing = False  # 标记是否已找到执行标准的 h2 标签

    for p in ori_data:
        if p.tag == 'h2' and "批准文号" in p.text:
            capturing = True  # 找到 h2 标签后，开始捕获 p 标签内容
            continue  # 跳到下一个元素以查找 p 标签

        if capturing and p.tag == 'p' and p.text:
            c2 = p.text.strip()
            text.append(c2)  # 将提取的内容添加到列表中
            break  # 找到 p 标签后，结束循环
    text = ''.join(text)
    return text if text else None  # 返回结果或 None


def process_data(cur_data):
    url = cur_data.get('url')
    html = cur_data.get("html")
    data = etree.HTML(html)
    title = get_title(data)
    content = get_content(data)
    ct = get_app(data)
    conpan = get_con(data)






    result = {
        "url" : url,
        "tt" : title,
        "cn" : content,
        "ct" : ct,
        "con" : conpan
    }
    return result



if __name__ == '__main__':
    with open("./data/六味地黄丸_六味地黄丸的作用_六味地黄丸的用法用量_六味地黄丸的不良反应_ 中国医药信息查询平台.html","r",encoding="utf-8") as file:
        cur_data = {
            "url" : "https://www.dayi.org.cn/drug/1022241.html",
            "html" : file.read()
        }
        pro_result = process_data(cur_data)
        print(json.dumps(pro_result, ensure_ascii=False, indent=4))
