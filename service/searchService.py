from game.websearch.SearchFromBC import bocha_web_search  # 博查搜索
from game.utils.process_web_model import extract_places_byModel, \
    extract_lng_lat_byModel  # 处理博查搜索的内容，利用大模型的总结能力得到松江大学城的建筑物
from game.utils.process_web_data import extract_snippets, extract_urls  # 对博查外部搜索的数据进行处理，得到url和content
from game.mapSearch.aroudplaces import amap_place_search  # 搜索地标周围的地点
from game.utils.process_map_data import extract_poi_names_and_photos  # 对地标周围点的具体数据进行处理，以得到关键数据
from game.utils.process_places_data import extract_songjiang_places  # 通过正则过滤得到松江大学城地标建筑物集合

"""
1.通过外部搜索得到关于question的urls
"""


def getUrlsFromWeb(question):
    temp_results = bocha_web_search(question)  # 得到在外部网站上关于question的资料
    urls_from_web = extract_urls(temp_results)  # 得到资料中的urls
    print("\nUrlsFromWeb:", urls_from_web)
    return urls_from_web


"""
2.通过外部搜索并给到大模型处理得到松江大学城里的建筑物
- 然后通过正则函数得到松江大学城的建筑物集合
"""


def getPlacesFromWeb(question):
    temp_results = bocha_web_search(question)  # 得到在外部网站上关于question的资料
    data_from_web = extract_snippets(temp_results)  # 得到资料中的snippets
    places = extract_places_byModel(data_from_web)  # 根据snippets丢给大模型总结出提到的地址
    songjiang_places = extract_songjiang_places(places)
    print("\nsongjiang_places:", songjiang_places)
    return songjiang_places


"""
3.得到所有候选建筑物的特点
"""


def getTraitsFromPlaces(question):
    temp_results = bocha_web_search(question)  # 得到在外部网站上关于question的资料
    data_from_web = extract_snippets(temp_results)  # 得到资料中的data
    print("\nTraitsOfPlace:", data_from_web)
    return data_from_web


"""
4.返回地点的经纬度
"""


def getLngAndLat_FromPlaces(question):
    temp_results = bocha_web_search(question)  # 得到在外部网站上关于question的资料
    data_from_web = extract_snippets(temp_results)  # 得到资料中的data
    lng_lat = extract_lng_lat_byModel(data_from_web)
    return lng_lat


"""
5.返回松江大学城周围的地点和图片
"""


def getAroud_smallplace_On_bigPlace(place_name):
    place_name = place_name + "(松江)"
    aroud_result = amap_place_search(place_name)
    print(aroud_result)
    small_names, small_name_photos = extract_poi_names_and_photos(aroud_result)  # 返回中心点的周围地点名称和图像内容""
    print(f"{place_name}周围的地标：{small_names}")
    print(f"{place_name}周围的地标的图像集合：{small_names}")
    return small_names, small_name_photos
