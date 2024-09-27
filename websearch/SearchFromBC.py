import requests
from game.utils.process_web_data import extract_urls, extract_snippets
from game.utils.process_web_model import extract_places_byModel

# 直接在代码中填入 API 密钥ai
BOCHA_API_KEY = 'xxxxxxxxxxxxxxxxx'


# 1.定义博查 Web 搜索的工具函数
def bocha_web_search(query, count=8):
    url = 'https://api.bochaai.com/v1/ai-search'  # 确保 API 端点正确
    headers = {
        'Authorization': f'Bearer {BOCHA_API_KEY}',  # 使用直接填入的博查 API 密钥
        'Content-Type': 'application/json'
    }
    # 设置请求体，查询和返回条数
    data = {
        'query': query,
        'count': count
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 检查是否成功
    if response.status_code == 200:
        return response.json()  # 返回解析后的 JSON 响应
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return {}


# 示例用法
if __name__ == "__main__":
    query = "松江大学城上海工程技术大学的经纬度坐标在哪？"
    # query = "上海工程技术大学有哪些建筑物？"
    result = bocha_web_search(query)
    print(result)
    # 提取所有的 snippet
    snippets = extract_snippets(result)
    print("Snippets:")
    for snippet in snippets:
        print(snippet)

    # 提取前 5 个 url
    urls = extract_urls(result)
    print("\nURLs:")
    for url in urls:
        print(url)

    # 对web外部搜索的相关信息进行处理返回范围更加小的信息（比如：松江大学城附近的建筑物）
    places = extract_places_byModel(snippets)

    print(places)
