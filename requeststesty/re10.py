import json
from lxml import etree
import re
from pyspark import SparkContext, SparkConf

def extract_id(url, pattern):
    """根据URL和正则表达式提取ID"""
    match = re.match(pattern, url)
    return match.group(1) if match else None

def get_title(node):
    """提取标题"""
    if node is None:
        return None
    ori_data = node.xpath("//div[@class='el-col el-col-24']/h1[@class='name font-bold']/text()")
    return ori_data[0] if ori_data else None

def get_company(node):
    """提取公司信息"""
    if node is None, return None
    ori_data = node.xpath("//div[@class='el-col el-col-24']/dl/text()")
    return ori_data[0] if ori_data else None

def get_approval_number(node):
    """提取批准文号"""
    if node is None:
        return None
    ori_data = node.xpath("//div[@class='el-col el-col-24']/li/text()")
    return ori_data[0] if ori_data else None

def get_content(node):
    """提取内容信息"""
    if node is None:
        return None

    content_data = node.xpath('.//div[@class="cont-2 tab-dm-2"]//*')
    content_text = []

    current_td = None
    current_td_de = []

    for elem in content_data:
        text = (elem.text or "").strip()

        if elem.tag == 'p' and text:
            content_text.append(text)
            continue

        if elem.tag == 'span' and "td" in elem.get("class", ""):
            if current_td and current_td_de:
                content_text.append(f"{current_td}: {' '.join(current_td_de)}")
            current_td = text
            current_td_de = []
            continue

        if elem.tag == 'var' and "td-details" in elem.get("class", ""):
            current_td_de.append(text)

        elif elem.tag == 'br' and current_td:
            tail_text = (elem.tail or "").strip()
            if tail_text:
                current_td_de.append(tail_text)

    if current_td and current_td_de:
        content_text.append(f"{current_td}: {' '.join(current_td_de)}")

    return '\n'.join(content_text)

def get_img_url(node):
    """提取图片URL"""
    img_elements = node.xpath("//img[@src]")
    img_urls = [img.get("src") for img in img_elements]
    return img_urls if img_urls else None

def process_url_data(cur_data, mode):
    """根据模式处理HTML内容，返回相应的结果"""
    data = json.loads(cur_data)
    url = data.get("url")
    html = data.get("html")
    node = etree.HTML(html)
    
    result = {
        "url": url,
        "tt": None,
        "ctt": {
            "content": None,
            "company": None,
            "approval_number": None,
            "img_url": None
        }
    }

    if mode == "title":
        result["tt"] = get_title(node)
        result["ctt"]["company"] = get_company(node)
        result["ctt"]["approval_number"] = get_approval_number(node)
    elif mode == "content":
        result["ctt"]["content"] = get_content(node)
        result["ctt"]["img_url"] = get_img_url(node)

    return json.dumps(result)

def get_url_id(cur_data, pattern):
    """获取URL中的ID，返回 (id, JSON数据) """
    data_str = json.loads(cur_data)
    url = data_str.get("url")
    url_id = extract_id(url, pattern)
    return (url_id, cur_data) if url_id else (None, None)

def combine_content(new_data, old_data):
    """合并相同URL ID的数据"""
    res1 = process_url_data(new_data, "content") if new_data else {}
    res2 = process_url_data(old_data, "title") if old_data else {}

    combined_result = {
        "url": json.loads(res1).get("url") or json.loads(res2).get("url"),
        "tt": json.loads(res2).get("tt"),
        "ctt": {
            "content": json.loads(res1).get("ctt", {}).get("content"),
            "company": json.loads(res2).get("ctt", {}).get("company"),
            "approval_number": json.loads(res2).get("ctt", {}).get("approval_number"),
            "img_url": json.loads(res1).get("ctt", {}).get("img_url")
        }
    }

    return json.dumps(combined_result)

if __name__ == '__main__':
    conf = SparkConf().setAppName("URL Processing").set("spark.driver.memory", "4g")
    sc = SparkContext(conf=conf)

    input1 = "hdfs://xx"
    input2 = "hdfs://yy"
    output = "hdfs://zz"

    pattern1 = r"https://www.cnblogs.com/(\d+)$"
    pattern2 = r"https://www.cnblogs.com/(?:introduce/)?(\d+)$"

    rdd1 = sc.textFile(input1).map(lambda x: get_url_id(x, pattern1)).filter(lambda x: x[0] is not None)
    rdd2 = sc.textFile(input2).map(lambda x: get_url_id(x, pattern2)).filter(lambda x: x[0] is not None)

    rdd_combined = rdd1.fullOuterJoin(rdd2).map(lambda x: combine_content(x[1][0], x[1][1]))

    rdd_combined.saveAsTextFile(output)
    
    sc.stop()
