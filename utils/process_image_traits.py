import json
import requests

"""
1.提取特征中的主要内容content
"""


def extract_traits_from_otherImages(response_json):
    # 将字符串转换为字典
    response_dict = json.loads(response_json)

    # 获取 content 的内容
    content = response_dict.get("choices", [])[0].get("message", {}).get("content", "")

    return content


"""
2.计算文本的向量
"""


def get_trait_embedding(input_text):
    url = "https://api.siliconflow.cn/v1/embeddings"

    payload = {
        "model": "BAAI/bge-large-zh-v1.5",
        "input": input_text,
        "encoding_format": "float"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer sk-kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk"
    }

    response = requests.post(url, json=payload, headers=headers)

    # 确认响应状态码是成功的
    if response.status_code == 200:
        response_data = response.json()
        # 提取embedding数据
        embeddings = response_data.get('data')[0].get('embedding')
        return embeddings
    else:
        print("Error:", response.status_code, response.text)
        return None


# 使用示例
input_text = "硅基流动embedding上线，多快好省的 embedding 服务，快来试试吧"
embedding_result = get_trait_embedding(input_text)
print(embedding_result)
