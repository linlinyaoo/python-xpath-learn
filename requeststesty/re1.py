from lxml import etree

# 假设html_content是您的HTML内容
html_content = '''<p>5、本品含酒萸肉以莫诺苷（C<sub>17</sub>H<sub>26</sub>O<sub>11</sub>）和马钱苷（C<sub>17</sub>H<sub>26</sub>O<sub>10</sub>）...</p>'''

# 解析HTML
root = etree.HTML(html_content)

# 提取<p>标签内的所有文本和<sub>标签的文本
# 注意：这里我们直接处理文本，不保留<sub>标签作为HTML元素
text_parts = []
for node in root.xpath('//p/node()'):
    if node.tag == 'sub':
        # 如果节点是<sub>，则添加带有特定标记的文本
        # 这里使用"[...]"作为<sub>文本的占位符
        text_parts.append(f"[{node.text}]")
    elif node.text:
        # 如果节点包含文本（但不是<sub>），则直接添加文本
        text_parts.append(node.text)

    # 将文本部分组合成一个字符串
final_text = ''.join(text_parts).strip()

print(final_text)