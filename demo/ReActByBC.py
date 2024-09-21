import os
import requests
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType
from langchain_core.runnables import Runnable

# 自定义模型类，用于与 SiliconFlow API 通信，继承 Runnable
class SiliconFlowModel(Runnable):
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def invoke(self, messages):
        payload = {
            "model": "internlm/internlm2_5-7b-chat",
            "messages": [{"role": "user", "content": messages}],
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.7,
            "stream": False
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        response_json = response.json()
        return response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

# 设置 API Keys
# os.environ["DASHSCOPE_API_KEY"] = '替换为你的DASHSCOPE_API_KEY'
os.environ["SERPAPI_API_KEY"] = '31a3c96f0ce535fd1b43117d3c9298c66753b6dae1da9074708f03ecc8282367'

# 初始化 SiliconFlow 模型
silicon_model = SiliconFlowModel(
    api_url="https://api.siliconflow.example/v1/models", 
    api_key="kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk"
)

# 加载工具
tools = load_tools(["serpapi"], llm=silicon_model)

# 初始化代理，使用 SiliconFlowModel
agent = initialize_agent(
    tools=tools,
    llm=silicon_model, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
)

# 使用 agent 执行任务
response = agent.run("今天星期几？历史上的今天发生了哪些大事？")

# 打印结果
print(response)
