from lxml import etree

html = '''
<ul>
    <li><span><em class="tejustify">通用名</em>：注射用氨曲南</span><span><em class="tejustify">批准文号</em>：国药准字H20093760</span></li>
    <li><span>
            <em class="tejustify">厂家</em>：
            <i title="海口市制药厂有限公司">
                海口市制药厂有限公司
            </i>
        </span>
        <span><em class="tejustify">有效期至</em>：2025-07-01</span></li>
    <li><span><em class="tejustify">件装数</em>：600</span><span><em class="tejustify">中包装</em>：10</span></li>
    <li><span><em class="tejustify">规格</em>：0.5g</span><span><em class="tejustify">库存</em>：1900</span></li>
    <li style="border:none"><span><em class="tejustify">单位</em>：瓶</span></li>
</ul>
'''

# 解析 HTML
tree = etree.HTML(html)

# 提取所有的 <li> 项
items = tree.xpath('//ul/li')

# 结果存储字典
result = []

# 遍历每个 <li> 并提取对应的 <span>、<em> 和 <i> 标签内容
for li in items:
    item = {}
    spans = li.xpath('.//span')

    for span in spans:
        # 获取 <em> 标签的文本作为 key
        key = span.xpath('.//em/text()')

        # 获取整个 <span> 的文本内容，包括 <i> 标签的内容
        value = span.xpath('string()')

        # 如果 <em> 标签有值，且整个 <span> 的文本不为空
        if key and value:
            key_text = key[0].strip().replace('：', '')  # 去除冒号和空格
            value_text = value.split('：', 1)[-1].strip()  # 获取冒号后面的内容

            # 如果 <i> 标签存在，则将其文本内容加上
            i_text = span.xpath('.//i/text()')
            if i_text:
                value_text = i_text[0].strip()  # 获取 <i> 标签中的文本，去掉空格

            item[key_text] = value_text

    result.append(item)
print(result)
# 输出结果
for item in result:
    print(item)
