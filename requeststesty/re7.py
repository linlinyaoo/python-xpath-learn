import json
from lxml import etree

def get_title(node):
    if node is None:
        return None
    title = node.xpath("//div[@class='el-col el-col-24']/h1[@class='name font-bold']/text()")
    return title[0].strip() if title else None

def get_content(node):
    if node is None:
        return None

    ori_data = node.xpath(".//div[@class='long-container']//*")
    text = []
    current_h2 = None
    current_paragraph = []

    for p in ori_data:
        if p.tag == 'h2':
            if current_paragraph:
                text.append(f"{current_h2}:\n\t" + "\n\t".join(current_paragraph))
                current_paragraph = []
            current_h2 = p.text.strip() if p.text else ''
        elif p.tag == 'p':
            paragraph_content = p.text.strip() if p.text else ''
            if paragraph_content:
                current_paragraph.append(paragraph_content)
        elif p.tag == 'sub':
            sub_html = etree.tostring(p, encoding='unicode', method='html').strip()
            if current_paragraph:
                current_paragraph[-1] += sub_html
            else:
                current_paragraph.append(sub_html)

    if current_paragraph:
        text.append(f"{current_h2}:\n\t" + "\n\t".join(current_paragraph))

    return '\n'.join(text)

def extract_section(node, section_title):
    if node is None:
        return None

    ori_data = node.xpath(".//div[@class='long-container']//*")
    capturing = False

    for p in ori_data:
        if p.tag == 'h2' and section_title in p.text:
            capturing = True
            continue

        if capturing and p.tag == 'p' and p.text:
            return p.text.strip()

    return None

def process_data(cur_data):
    url = cur_data.get('url')
    html = cur_data.get("html")
    data = etree.HTML(html)

    title = get_title(data)
    content = get_content(data)
    execution_standard = extract_section(data, "执行标准")
    approval_number = extract_section(data, "批准文号")

    result = {
        "url": url,
        "title": title,
        "content": content,
        "execution_standard": execution_standard,
        "approval_number": approval_number
    }

    return result

if __name__ == '__main__':
    with open("./data/六味地黄丸_六味地黄丸的作用_六味地黄丸的用法用量_六味地黄丸的不良反应_ 中国医药信息查询平台.html", "r", encoding="utf-8") as file:
        cur_data = {
            "url": "https://www.dayi.org.cn/drug/1022241.html",
            "html": file.read()
        }
        processed_result = process_data(cur_data)
        print(json.dumps(processed_result, ensure_ascii=False, indent=4))
