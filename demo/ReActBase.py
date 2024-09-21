import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_community.llms import Tongyi

# 设置API密钥
os.environ["SERPAPI_API_KEY"] = "31a3c96f0ce535fd1b43117d3c9298c66753b6dae1da9074708f03ecc8282367"
os.environ["DASHSCOPE_API_KEY"] = "sk-d07d9d5c4d8d4158abbaf45a40c10042"

# 导入所需的库和模型
DASHSCOPE_API_KEY = "sk-d07d9d5c4d8d4158abbaf45a40c10042"
llm = Tongyi(dashscope_api_key="sk-d07d9d5c4d8d4158abbaf45a40c10042", model="qwen-plus")

# 加载工具
tools = load_tools(["serpapi"], llm=llm)

# 初始化代理
agent = initialize_agent(tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)

# 运行代理
response = agent.run(
    "假设你是一个特征分析师，你能够根据特征分析出具体位置，请根据以下特征告诉我具体地址?（确定具体地理位置。比如：xxx学校的xx教学楼、xxx学校的xxx图书馆、xxx地区的xxx办公楼、xxx地区的xxx餐厅、xxx地区的xxx娱乐城等等。注意：回复不能模棱两可，不能回复自己不知道，需要根据以下特征坚定的回答一处地方，并逐步思考）前提：该具体位置位于上海市松江大学城的某处地方，1. 建筑设计：该建筑物的整体外形设计为独特的M型结构，墙体颜色为白色，给人一种现代和前卫的感觉。这种设计可能意味着该建筑是为了某种特定的功能或目的而建，如艺术展览、会议中心或其他公共设施。 2. 玻璃幕墙：从图片中可以看到，建筑物的一部分使用了大面积的玻璃幕墙。这可能意味着内部空间需要充足的自然光，或者是为了展示外部景观。 3. 周围环境：该建筑位于一个开阔的区域，前面有一个湖泊或大型池塘。湖边有绿色的草坪和树木，为这个区域提供了一个宁静的环境。此外，远处还有一些低矮的建筑和道路，暗示该地点可能是城市中的一个公园或休闲区。 4. 天气：天空是晴朗的蓝色，没有云彩，说明这是一个好天气的日子。这样的天气可能会吸引许多人到这个地方游玩或进行户外活动。 5. 具体位置在上海市江大学城的某处地方 ")
print(response)
