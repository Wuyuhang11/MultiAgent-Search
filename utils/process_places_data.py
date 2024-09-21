import re


def extract_songjiang_places(text):
    # 定义正则表达式来匹配序号后面的内容，直到遇到空格为止
    pattern = r'\d+\.\s*([^\s]+)'  # 匹配格式如 '1. 内容'

    # 使用 re.findall 提取所有符合条件的内容
    content = re.findall(pattern, text)

    # 返回一个包含唯一内容的集合
    return set(content)


# 示例文本
text = '''1. 上海工程技术大学松江校区
2. 东华大学
3. 华东政法大学

根据所提供的数据，仅明确提到了上海工程技术大学松江校区位于松江大学城内，但依据松江大学城普遍认知，东华大学和华东政法大学也位于松江大学城内。其他具体建筑物或校区未在数据中被明确提及。'''

# 调用函数并输出结果
content_after_number = extract_songjiang_places(text)
print(content_after_number)
