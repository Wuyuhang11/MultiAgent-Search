import tempfile
import json
import os

"""
1.将相似度最高的信息存储到一个文件当中
"""


def write_top_similarities_to_file(top_3_similarities, save_path):
    """
    将前三个相似度最高的地标信息及其特征写入指定路径的临时文件中。

    参数:
    - top_3_similarities: 包含地标、相似度和特征的前三个相似度信息列表
    - save_path: 保存临时文件的路径

    返回:
    - temp_file_name: 临时文件的完整路径
    """
    # 确保保存路径存在
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 将前三个相似度最高的地标信息及其特征写入临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8',
                                     dir=save_path) as temp_file:
        for small_name, similarity, big_place, traits in top_3_similarities:
            # 写入 small_place, similarity, 和 traits 信息
            temp_file.write(f"Small Place: {small_name}\n")
            temp_file.write(f"Similarity: {similarity}\n")
            temp_file.write(f"Traits: {json.dumps(traits, ensure_ascii=False, indent=4)}\n")

            # 写入分隔线
            divider = '---------------------------'
            temp_file.write(f"{divider}\n")

        # 保存临时文件的路径
        temp_file_name = temp_file.name
    print(f"前三个相似度最高的小地标信息已写入临时文件：{temp_file_name}")
    return temp_file_name
