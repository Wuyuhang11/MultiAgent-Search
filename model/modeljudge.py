import os
from langchain_community.llms import Tongyi
from langchain_core.prompts import PromptTemplate
import chardet

# 1. 设置API密钥
os.environ["DASHSCOPE_API_KEY"] = "xxxxxxxxxxxxxxxxxx"

# 2. 导入所需的库和模型
DASHSCOPE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxx"
llm = Tongyi(dashscope_api_key="sxxxxxxxxxxxxxxxxxxxxxx", model="qwen-plus")

# 3. 设置template
template = """你现在扮演的是一名地址特征比较工程师，请利用传入的图片主特征{maintraits}，与文件内容{filecontents}中的Small Place的Traits进行比较，分析其原因，返回特征最接近的Small Place。

要求：
1. 以建筑特点为主
2. 根据文件内容返回一个你认为特征最接近的Small Place
3. 结果格式示例：
   分析：xxxxx的建筑风格与图片主特征最相近，特征为：xxxx，由此可知xxxx。而xxx的建筑风格与xxx并不相近，因为xxxx，所以xxx为最相似的地点

图片主特征： {maintraits}
文件内容：{filecontents}
"""

prompt = PromptTemplate.from_template(template)


# 1.根据主特征和候选特征进行judge
def judge_byModel(maintraits, file_path):
    # 自动检测文件编码
    with open(file_path, 'rb') as f:
        raw_data = f.read()  # 读取文件的二进制内容
        result = chardet.detect(raw_data)  # 检测编码
        encoding = result['encoding']  # 获取检测到的编码

    # 使用检测到的编码读取文件内容
    with open(file_path, 'r', encoding=encoding) as f:
        filecontents = f.read()  # 读取整个文件内容

    chain_input = {"maintraits": maintraits, "filecontents": filecontents}

    chain = prompt | llm
    judge_content = chain.invoke(chain_input)
    return judge_content
