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




from lxml import etree

html_content = '''<div id="con_one_2" style="display: block;">
<p style="...">通用名称：奥美拉唑肠溶胶囊</p>
<p style="...">&nbsp;&nbsp;商品名称：奥美拉唑肠溶胶囊(立卫克)</p>
<p style="...">&nbsp;&nbsp;拼音全码：AoMeiLaZuoChangRongJiaoNang(LiWeiKe)</p>
<p style="..."><span style="font-weight: bold;">【主要成份】</span>&nbsp;本品主要成份为：奥美拉唑。</p>
<p style="..."><span style="font-weight: bold;">【成 份】</span></p>
<p style="...">&nbsp;&nbsp;化学名： S-甲氧基-2-（（（4-甲氧基-3，S-二甲基-2 -吡啶基）甲基）亚磺酰基）-1H-苯并咪唑</p>
...
</div>'''

# 使用lxml解析HTML
tree = etree.HTML(html_content)
div = tree.xpath('//div[@id="con_one_2"]')[0]

# 初始化字典存储提取数据
data = {}

# 提取所有的<p>标签
paragraphs = div.xpath('.//p')

for p in paragraphs:
    bold_text = p.xpath('.//span[@style="font-weight: bold;"]/text()')
    full_text = p.xpath('string()').strip()
    
    if bold_text:
        # 获取【...】格式的标签内容
        key = bold_text[0].strip("【】")
        # 获取【...】后面的值
        value = full_text.split("】")[-1].strip()
        data[key] = value
    else:
        # 处理没有【】的情况
        key, value = full_text.split("：", 1)
        data[key.strip()] = value.strip()

# 打印提取的内容
for key, value in data.items():
    print(f'{key}: {value}')


def extract_info(html_data, sel):
    result = []

    # 解析 HTML 数据
    from lxml import etree
    tree = etree.HTML(html_data)

    # 获取包含数据的 li 元素
    items = tree.xpath('//li')  # 假设 <li> 标签包含需要提取的信息

    for li in items:
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

                # 根据输入的 sel 来决定是否提取这个字段
                if key_text == sel:
                    result.append({key_text: value_text})

    return result

# 使用示例
html_data = """<html>...</html>"""  # 你的 HTML 数据
sel = '通用名称'  # 你要提取的字段，例如 '通用名称', '批准文号' 或 '生产企业'
info = extract_info(html_data, sel)
for item in info:
    print(item)
