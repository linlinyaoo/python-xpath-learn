import json
import re

# 初始化计数器
non_empty_content_count = 0

# 定义一个函数来提取 `ing` 部分
def extract_ing(content):
    # 如果 content 是空列表 [] 或者空字符串，返回空值
    if not content or content == "[]":
        return ""
    
    # 使用正则表达式来提取 ing 的值
    match = re.search(r'\[ing:\s*(.*?)\]', content)
    if match:
        return match.group(1)  # 返回 ing 的值
    return ""

# 读取 JSON 文件
with open('data.json', 'r', encoding='utf-8') as file:
    for line in file:
        # 将每行 JSON 转换为 Python 字典
        record = json.loads(line)

        # 获取 content 字段
        content = record.get("ctt", {}).get("content", "")

        # 提取 content 中的 `ing` 值
        ing_value = extract_ing(content)

        # 判断 ing_value 是否非空
        if ing_value:
            non_empty_content_count += 1

# 输出非空 ing 字段的统计结果
print(f"非空 ing 字段的总数为: {non_empty_content_count}")
