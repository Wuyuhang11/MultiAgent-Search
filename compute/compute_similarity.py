from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  # 导入余弦相似度函数
from game.utils.process_image_traits import get_trait_embedding  # 得到特征文本的向量
import numpy as np

"""
1.通过TF-IDF计算词频的方式来计算text1和text2之间的相似度
"""


def calculate_tfidf_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    corpus = [text1, text2]
    vectors = vectorizer.fit_transform(corpus)
    similarity = cosine_similarity(vectors)
    return similarity[0][1]  # 返回第一个文本和第二个文本之间的相似度


"""
2.计算text1和text2的相似度
"""


def calculate_embedding_cosine_similarity(text1, text2):
    # 1.得到文本的向量
    embedding1 = get_trait_embedding(text1)
    embedding2 = get_trait_embedding(text2)
    # 2.将列表转换为numpy数组，方便执行向量操作
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    # 3.计算两个向量的点积
    dot_product = np.dot(vec1, vec2)

    # 4.计算两个向量的欧几里得范数【即表示向量的长度和大小】
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    # 5.计算余弦相似度
    cosine_sim = dot_product / (norm_vec1 * norm_vec2)

    # 6.返回保留六位小数的结果
    return round(cosine_sim, 6)


# # 示例
text1 = """'1. **建筑风格**：
   - 这些建筑具有独特的几何形状，尤其是三角形和多边形的结构。
   - 建筑物的外观设计独特，可能是由玻璃和混凝土等材料构成。

2. **环境**：
   - 周围有绿化带和树木。
   - 有水体和桥梁。

3. **地理位置**：
   - 这些建筑位于一个较大的区域，周围有其他建筑物和设施。
   - 远处可以看到山脉。'"""

text2 = """1. **建筑风格**：
   - 图像中的建筑具有独特的几何形状，主要由三角形和多边形构成，呈现出现代主义和未来主义的风格。
   - 建筑物的设计独特，具有明显的尖顶和斜面，给人一种科技感和创新感。

2. **环境**：
   - 建筑周围有广阔的绿地和水体，环境优美，绿化覆盖率高。
   - 建筑物周围有道路和桥梁，交通便利，周围还有其他建筑物和设施，形成一个完整的区域。

3. **地理位置**：
   - 建筑位于一个城市或大学校园内，周围有其他建筑物和设施，表明这是一个有人居住和活动的区域。
   - 建筑物的地理位置可能是一个重要的地标或文化中心，吸引了大量的游客和参观者。"""
similar_points = calculate_embedding_cosine_similarity(text1, text2)
print("相似度：", similar_points)
