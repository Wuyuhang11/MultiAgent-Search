import os
import requests
from langchain.agents import initialize_agent, AgentType
from langchain.agents import load_tools
from langchain_core.runnables import Runnable
from langchain_community.llms import Tongyi

# 自定义模型类，用于与 SiliconFlow API 通信，继承 Runnable
class SiliconFlowModel(Runnable):
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    # 修改 invoke 方法，添加 *args 和 **kwargs 捕获所有额外参数
    def invoke(self, messages, *args, **kwargs):
        # 检查消息是否是 StringPromptValue，如果是，则转换为字符串
        if isinstance(messages, StringPromptValue):
            messages = str(messages)  # 将 StringPromptValue 转换为字符串
        
        payload = {
            "model": "internlm/internlm2_5-7b-chat",
            "messages": [{"role": "user", "content": messages}],  # 确保 messages 是字符串
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

       # 处理生成结果
        result = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

        # 如果 kwargs 中有 stop 参数，处理截断逻辑
        stop = kwargs.get('stop', None)
        if stop:
            for token in stop:
                result = result.split(token)[0]

        return result

# 设置 API Keys
# os.environ["DASHSCOPE_API_KEY"] = '替换为你的DASHSCOPE_API_KEY'
os.environ["SERPAPI_API_KEY"] = 'xxxxxxxxxxxx'

# 初始化 SiliconFlow 模型
silicon_model = SiliconFlowModel(
    api_url="https://api.siliconflow.example/v1/models", 
    api_key="sk-kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk"
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
response = agent.run("今天星期几？历史上的今天发生了哪些大事？".__str__)

# 打印结果
print(response)
