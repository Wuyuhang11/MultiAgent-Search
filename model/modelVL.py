from openai import OpenAI
import os
from game.utils.image_read import encode_image

# 设置环境变量，存储 API 密钥
os.environ["DASHSCOPE_API_KEY"] = "sk-d07d9d5c4d8d4158abbaf45a40c10042"

"""
1.通过tongyi-VL识别图像位置
"""


def get_image_place(image_path, user_question):
    base64_image = encode_image(image_path)
    client = OpenAI(
        api_key="sk-d07d9d5c4d8d4158abbaf45a40c10042",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-vl-max-0809",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": user_question
                    }
                ]
            }
        ]
    )
    print(completion.model_dump_json())  # 如果你需要以 JSON 格式打印输出，这里假设方法名正确
    return completion.model_dump_json()


"""
2.通过tongyi-VL识别图像特征
"""


def get_image_traits(image_path):
    base64_image = encode_image(image_path)
    client = OpenAI(
        api_key="sk-d07d9d5c4d8d4158abbaf45a40c10042",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-vl-max-0809",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "假设你是图像特征提取小助手，已知传入的图像来自上海市松江大学城的某处地方，请帮我总结上述图像的特征【只需要阐述图像的特征（包括建筑风格、环境、地理位置三个方面），无需进行过度推理。回答内容如：\n\n"
                                "1. **建筑风格**：\n"
                                "   - 这些建筑具有独特的几何形状，尤其是三角形和多边形的结构。\n"
                                "   - 建筑物的外观设计独特，可能是由玻璃和混凝土等材料构成。\n\n"
                                "2. **环境**：\n"
                                "   - 周围有绿化带和树木。\n"
                                "   - 有水体和桥梁。\n\n"
                                "3. **地理位置**：\n"
                                "   - 这些建筑位于一个较大的区域，周围有其他建筑物和设施。\n"
                                "   - 远处可以看到山脉。\n\n】"
                    }
                ]
            }
        ]
    )
    print(completion.model_dump_json())  # 如果你需要以 JSON 格式打印输出，这里假设方法名正确
    return completion.model_dump_json()


"""
3.得到其余被比较图像的特征
"""


def get_other_image_traits(image_paths):
    # 如果 image_paths 是空集合，则直接退出函数
    if not image_paths:
        return

    # 动态生成 messages 的内容，根据 image_paths 的数量创建多个 image_url
    image_messages = []

    for image_url in image_paths:
        base64_image = encode_image(image_url)
        image_messages.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })

    # 在最后添加文本信息
    image_messages.append({
        "type": "text",
        "text": "假设你是图像特征提取小助手，已知传入的图像来自同一个地方，请帮我总结上述图像的特征【只需要阐述图像的特征（包括建筑风格、环境、地理位置三个方面），无需进行过度推理。示例：\n\n"
                "1. **建筑风格**：\n"
                "   - xxxxxx。\n"
                "   - xxxx。\n\n"
                "2. **环境**：\n"
                "   - xxxxx。\n"
                "   - xxxxxx。\n\n"
                "3. **地理位置**：\n"
                "   - xxxxxx。\n"
                "   - xxxxxxx。\n\n】"

    })

    # 创建 OpenAI 客户端
    client = OpenAI(
        api_key="sk-d07d9d5c4d8d4158abbaf45a40c10042",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 调用 OpenAI 的 API，生成 chat completion
    completion = client.chat.completions.create(
        model="qwen-vl-max-0809",
        messages=[
            {
                "role": "user",
                "content": image_messages
            }
        ]
    )

    # 输出 API 返回的结果
    print(completion.model_dump_json())
    return completion.model_dump_json()


# 示例使用997875/1000000
if __name__ == "__main__":
    image_paths = ['http://store.is.autonavi.com/showpic/0d1506fe0980cbe468095fb32ccf4023',
                   'http://store.is.autonavi.com/showpic/c766361b076ce5789f2bc7cf848e2307',
                   'http://store.is.autonavi.com/showpic/466f5ba72b508d7469c2f80b07dfee2f']
    # image_path = "D://Answer//python-learning//Fuction//game//sues02.png"
    other_images_traits = get_other_image_traits(image_paths)
    print(other_images_traits)
