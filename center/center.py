from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from game.service.searchService import getPlacesFromWeb, getUrlsFromWeb  # 通过外部搜索得到资料的urls和松江大学城的places
from game.service.searchService import getAroud_smallplace_On_bigPlace
from game.service.ImageService import getTraitsFrom_Images, getTraitsFrom_Image  # 业务实现类：得到图像特征
from game.compute.compute_similarity import calculate_embedding_cosine_similarity, \
    calculate_tfidf_cosine_similarity  # 计算特征之间的相似度
from flask_cors import CORS
from gevent import pywsgi
import shutil  # 导入 shutil 模块用于文件操作
import tempfile
import json
from game.utils.similarity_read import write_top_similarities_to_file  # 将相似度top-3的信息写入文件
from game.model.modeljudge import judge_byModel  # 进行特征的最后决策
from game.utils.process_set_tolist import convert_sets_to_lists  # 将set数据转为list数据
from game.tts.text_to_video import generate_audio  # 根据文本生成音频

app = Flask(__name__)
# app.json.ensure_ascii = False  # 解决中文乱码问题
app.config['JSON_AS_ASCII'] = False
CORS(app, resources={r"/*": {"origins": "*"}})

# 环境配置
app.config['UPLOAD_FOLDER'] = 'uploads'  # 确保这个文件夹存在或在代码中创建它
app.config['UPLOAD_FOLDER'] = 'image_temp'
# API密钥配置
os.environ["DASHSCOPE_API_KEY"] = "sk-d07d9d5c4d8d4158abbaf45a40c10042"
save_path = '..//tempfile//'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# 上传图像和问题得到响应
@app.route('/upload', methods=['POST'])
def upload_file():
    print("你好呀~")
    # 1.上传文件模块
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({"error": "File not supported"}), 400

    original_filename = secure_filename(file.filename)
    timestamp_ms = int(datetime.now().timestamp() * 1000)
    filename = f"{timestamp_ms}_{original_filename}"
    original_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # 再次确认目录存在
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(original_file_path)

    # 创建新的文件路径
    new_filename = f"processed_{filename}"
    new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

    # 复制文件到新路径
    shutil.copy(original_file_path, new_file_path)
    print(f"临时文件名：{new_filename}")
    print(f"临时文件URL：{new_file_path}")

    # 1.4.获取用户提问
    user_question = request.form['question']
    print("用户问题：", user_question)

    # 2.得到主图像特征
    main_traits = getTraitsFrom_Image(new_file_path)
    print("该图像的特征如下：", main_traits)  # 【1.主图特征】

    # 3.首先获取松江大学城内的地标建筑物，缩小范围
    first_question = "上海市松江区松江大学城内有哪些建筑物？"
    urls_from_web = getUrlsFromWeb(first_question)  # 通过外部搜索得到关于question的urls集合 # 【2.参考文献】
    songjiang_places = getPlacesFromWeb(first_question)  # 得到松江大学城里的建筑物集合 # 【3.附近地点】

    big_places_dict = {}  # 初始化一个大集合big_places_dict，元素为每一个bigplace
    max_similarities = []  # 初始设置为-1，得到最大相似度
    small_names = []
    small_name_photos = {}

    # 4.计算得到相似度最高的小地标名称
    for big_place in songjiang_places:  # 【3.大地点】
        small_names, small_name_photos = getAroud_smallplace_On_bigPlace(big_place)  # 得到小地标的名称和小地标的图片集合

        # 为当前大地标创建一个字典来存储每个小地标及其与主图像的相似度
        small_places = {}

        for small_name, small_photos in small_name_photos.items():
            print(f"{small_name}：{small_photos}")  # 【4.大地点的小地点】
            if not small_photos:
                print(f"{small_name} 没有可用的照片，跳过此地标")
                continue
            try:
                small_traits = getTraitsFrom_Images(small_photos)  # 得到小地标的图像特征
                print(f"{small_name}的地图特征为：{small_traits}")
                small_and_main_similarity = calculate_embedding_cosine_similarity(main_traits, small_traits)
                print(f"{small_name}与图像特征的相似度为：{small_and_main_similarity}")
                small_places[small_name] = small_traits
            except Exception as e:
                print(f"处理 {small_name} 的图像时发生错误: {e}")
                continue  # 遇到错误时跳过此地标

            # 更新整体最高相似度列表及其对应的小地标名称、特征及大地标
            max_similarities.append((small_name, small_and_main_similarity, big_place, small_traits))

        # 将当前大地标及其所有小地标的相似度信息存入字典
        big_places_dict[big_place] = small_places

    # 5.对相似度列表按照相似度值进行降序排序
    max_similarities.sort(key=lambda x: x[1], reverse=True)

    # 6.只取前三个
    top_3_similarities = max_similarities[:3]

    # 打印所有地标中相似度最高的三个小地标信息
    if top_3_similarities:
        for idx, (small_name, similarity, big_place, traits) in enumerate(top_3_similarities, 1):
            print(f"第{idx}名：小地标是：{small_name}，位于大地标 {big_place}，相似度为：{similarity}，特征为：{traits}")

    # 7.将前三个相似度最高的地标信息及其特征写入临时文件
    top3_file = write_top_similarities_to_file(top_3_similarities, save_path)

    # 9.给到决策大模型进行参考，得到最后的answer
    judge_content = judge_byModel(main_traits, top3_file)
    print(f"最后决策：{judge_content}")

    # 10.根据JudgeContent内容生成音频
    video_path = generate_audio(judge_content)
    print(f"音频路径：{video_path}")

    # 11.返回相似度最高的前三个地标信息，按相似度排序后标上序号
    response = [
        {
            "rank": idx,  # 直接使用 idx，因为 enumerate 从 1 开始
            "small_place": small_name,
            "big_place": big_place,
            "similarity": similarity,
            "traits": convert_sets_to_lists(traits)
        }
        for idx, (small_name, similarity, big_place, traits) in enumerate(top_3_similarities, start=1)
    ]

    return jsonify({
        "main_traits": convert_sets_to_lists(main_traits),  # 传入图像的特征
        "first_question": first_question,  # 问题
        "candidate_big_places": convert_sets_to_lists(songjiang_places),  # 得到松江大学城里的大地点集合
        "search_around_traits": convert_sets_to_lists(big_places_dict),  # 大地点下面的小地点特征
        "candidate": convert_sets_to_lists(response),  # 候选地点和特征
        "judge_content": judge_content,  # 最后的决策
        "video_path": video_path  # 音频路径
    })


if __name__ == '__main__':
    app.debug = True
    server = pywsgi.WSGIServer(('0.0.0.0', 8081), app)
    server.serve_forever()
