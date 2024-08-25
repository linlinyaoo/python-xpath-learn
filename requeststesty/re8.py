import json
from lxml import etree
import re
def get_title(node,select_tile=None):
    if node is None:
        return None
    title_data = node.xpath('.//div[@class="details-right-drug"]')
    title_text = None
    selected_texts = []
    for elem in title_data[0].xpath('./p'):
        if 'Explain' not in elem.get("class", "") and elem.text:
            title_text = elem.text.strip()
            break
    for li in title_data[0].xpath('./ul/li'):
        li_text = li.xpath('string()').strip()  # Use string() to get all the text inside the <li>
        if select_tile and isinstance(select_tile, str) and select_tile in li_text:
            selected_texts.append(li_text)
    return title_text, selected_texts

# def get_content(node):
#     if node is None:
#         return None
#     content_data = node.xpath('.//div[@class="cont-2 tab-dm-2"]//*')
#     content_text = []
#     for elem in content_data:
#         print(elem.tag)
#         text = elem.text.strip() if elem.text else ""  # 确保只有非空文本被添加
#         if elem.tag == 'p' and text:
#             content_text.append(text)
#         elif elem.tag == 'span' and "td" in elem.get("class", "") and text:
#             content_text.append(text)
#         elif elem.tag == 'var' and "td-details" in elem.get("class", "") and text:
#             content_text.append(text)
#         elif elem.tag == 'br':
#             # if content_text and content_text[-1] != "\n":
#             #     content_text.append("\n")  # 仅在前一个元素不是换行符时添加换行符
#                 # 提取br标签后的文本内容
#             tail_text = (elem.tail or "").strip()
#             if tail_text:
#                 content_text.append(tail_text)
#     return content_text


def get_content(node):
    if node is None:
        return None

    # 获取目标 div 内的所有元素
    content_data = node.xpath('.//div[@class="cont-2 tab-dm-2"]//*')
    content_text = []

    current_td = None  # 用于存储当前的 td 文本
    current_td_de = []  # 用于存储当前的 td-details 文本列表

    for elem in content_data:
        text = (elem.text or "").strip()  # 获取元素内部的文本内容

        if elem.tag == 'p' and text:
            content_text.append(text)
            continue

        if elem.tag == 'span' and "td" in elem.get("class", ""):
            # 如果存在上一个 td，先将其内容保存
            if current_td and current_td_de:
                content_text.append(f"{current_td}: {' '.join(current_td_de)}")

            # 重置 current_td 和 current_td_de
            current_td = text
            current_td_de = []
            continue

        if elem.tag == 'var' and "td-details" in elem.get("class", ""):
            current_td_de.append(text)

        elif elem.tag == 'br' and current_td:
            tail_text = (elem.tail or "").strip()
            if tail_text:
                current_td_de.append(tail_text)

    # 处理最后一个 td 的内容
    if current_td and current_td_de:
        content_text.append(f"{current_td}: {' '.join(current_td_de)}")

    return content_text

def pro_duce(cur_data):
    url = cur_data.get("url")
    html = cur_data.get("html")
    data = etree.HTML(html)
    # Extract the title, production company, and approval number
    title, _ = get_title(data)
    _, production_company = get_title(data, "生产企业")
    _, approval_number = get_title(data, "批准文号")
    content = get_content(data)
    result = {
        "url": url,
        "title": title,
        "production_company": re.sub("生产企业：","",production_company[0] if production_company else None),
        "approval_number": re.sub("批准文号：","",approval_number[0] if approval_number else None),
        "content" : content
    }
    return result


if __name__ == '__main__':
    with open("./data/大幸药品株式会社康腹止泻片价格_说明书_功效与作用_用法用量_副作用_医生点评_用药指导_快速问医生.html","r",encoding="utf-8") as file:
        cur_data = {
            'url': 'https://yp.120ask.com/detail/202520.html',
            'html': file.read()
        }
        result = pro_duce(cur_data)
        print(json.dumps(result, ensure_ascii=False,indent=4))