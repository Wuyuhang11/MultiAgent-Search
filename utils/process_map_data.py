def extract_poi_names_and_photos(response):
    """
    提取API响应中的POI名称和对应的照片信息，并收集所有POI的照片到一个大集合中。

    参数:
        response (dict): 高德API返回的响应数据

    返回:
        names_set (set): 所有POI名称的集合
        name_photos_dict (dict): 每个POI名称对应的照片集合
        all_photos_set (set): 所有POI的照片的大集合
    """
    pois = response.get('pois', [])  # 获取POI列表，默认为空列表

    names_set = set()  # 存储所有POI名称的集合
    name_photos_dict = {}  # 存储每个POI名称对应的照片集合
    all_photos_set = set()  # 存储所有POI的照片（大集合）

    for poi in pois:
        # 提取名称
        name = poi.get('name')
        if name:
            names_set.add(name)  # 将名称添加到集合中

            # 提取photos
            photos = poi.get('photos', [])
            photo_urls = {photo.get('url') for photo in photos if 'url' in photo}  # 提取所有照片的URL

            # 更新 name_photos_dict
            if name in name_photos_dict:
                name_photos_dict[name].update(photo_urls)  # 如果name已经存在，更新它的照片集合
            else:
                name_photos_dict[name] = photo_urls  # 否则，创建新的照片集合

            # 将这些照片URL加入总的照片集合中
            all_photos_set.update(photo_urls)

    return names_set, name_photos_dict


# # 示例API响应
# response = {
#     "pois": [
#         {
#             "name": "上海工程技术大学松江校区",
#             "photos": [
#                 {"url": "http://photo1.com/photo1.jpg"},
#                 {"url": "http://photo2.com/photo2.jpg"}
#             ]
#         },
#         {
#             "name": "北京大学",
#             "photos": [
#                 {"url": "http://photo3.com/photo3.jpg"}
#             ]
#         },
#         {
#             "name": "复旦大学",
#             "photos": []  # 没有照片的POI
#         },
#         {
#             "name": "上海工程技术大学松江校区",  # 同一个名称，更多照片
#             "photos": [
#                 {"url": "http://photo4.com/photo4.jpg"}
#             ]
#         }
#     ]
# }
#
# # 提取POI名称和照片
# names, name_photos = extract_poi_names_and_photos(response)
#
# # 打印结果
# print("POI名称集合:", names)
# print("POI名称与对应照片集合:")
# for name, photos in name_photos.items():
#     print(f"{name}: {photos}")
#
# print("\n所有POI的照片集合:")
# print(name_photos)
