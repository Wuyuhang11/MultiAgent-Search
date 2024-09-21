import os
from langchain_community.llms import Tongyi
from langchain_core.prompts import PromptTemplate

# 1. 设置API密钥
os.environ["SERPAPI_API_KEY"] = "31a3c96f0ce535fd1b43117d3c9298c66753b6dae1da9074708f03ecc8282367"
os.environ["DASHSCOPE_API_KEY"] = "sk-d07d9d5c4d8d4158abbaf45a40c10042"

# 2. 导入所需的库和模型
DASHSCOPE_API_KEY = "sk-d07d9d5c4d8d4158abbaf45a40c10042"
llm = Tongyi(dashscope_api_key="sk-d07d9d5c4d8d4158abbaf45a40c10042", model="qwen-plus")

# 3. 设置template
template = """你现在扮演的是一名专业的信息提取工程师。请根据以下数据中提取并列举出松江大学城内的所有建筑物。请确保结果清晰且按编号列出。

要求：
1. 只列出建筑物的名称，无需加其他任何内容。
2. 每个建筑物一行，用数字序号标记。
3. 结果格式示例：
   1. 上海工程技术大学
   2. 东华大学
   3. 华东政法大学

数据如下: {question}
"""
template2 = """你现在扮演的是一名专业的信息提取工程师。请根据以下数据中提取出经纬度，并只需要返回经纬度即可。

要求：
1. 只列出经纬度，无需加其他任何内容。
2. 经度在前，纬度在后
3. 结果格式示例：
   121.205007,31.056050

数据如下: {question}
"""

prompt = PromptTemplate.from_template(template)
prompt2 = PromptTemplate.from_template(template2)

# 1.处理网络搜索后的数据，返回指定格式的建筑物
def extract_places_byModel(question):
    chain = prompt | llm
    places = chain.invoke({"question": question})
    return places

# 2.返回地理位置的经纬度
def extract_lng_lat_byModel(question):
    chain = prompt2 | llm
    lng_lat = chain.invoke({"question": question})
    return lng_lat