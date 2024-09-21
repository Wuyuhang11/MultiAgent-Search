import requests
from game.utils.process_map_data import extract_poi_names_and_photos

"""
 1.调用高德地图API的文本搜索接口，获取指定地点信息。

 参数:
     keywords (str): 查询的关键字，例如 "北京大学"。
     city (str): 城市名称，例如 "beijing"。
     key (str): 高德地图的API密钥。
     types (str): 查询POI类型，可选，默认为None。
     citylimit (bool): 是否限制返回结果为指定城市，默认为False。
     offset (int): 每页结果数，强烈建议不超过25，默认为20。
     page (int): 当前页数，默认为1。
     extensions (str): 返回结果控制，默认为'all'。

 返回:
     dict: API返回的结果，包含地点的详细信息。
 """
def amap_place_search(keywords, city=None, types=None, citylimit=False, offset=20, page=1, extensions='all'):

    base_url = "https://restapi.amap.com/v3/place/text"

    # 请求参数
    params = {
        "keywords": keywords,
        "city": city,
        "key": "04708221844d5c25b001370f52a83791",
        "types": types,
        "citylimit": "true" if citylimit else "false",
        "offset": offset,
        "page": page,
        "extensions": extensions
    }

    # 发送GET请求
    response = requests.get(base_url, params=params)

    # 判断请求是否成功
    if response.status_code == 200:
        return response.json()  # 返回JSON格式的响应
    else:
        return {"error": f"请求失败，状态码: {response.status_code}"}


# 示例使用
if __name__ == "__main__":
    keywords = "上海工程技术大学(松江)"

    result = amap_place_search(keywords)
    names_set, name_photos_dict, all_photos_set = extract_poi_names_and_photos(result)  # 返回上海工程技术大学周围的地标
    print("\n" + keywords + "附近的地点为：", names_set)
    print("\n" + keywords + "附近的地点为的图片为：", name_photos_dict)
