import asyncio
import edge_tts
import os


async def text_to_speech(text: str, voice: str, output_file: str) -> None:
    """将文本转换为语音并保存为音频文件。"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


def generate_audio(text: str, voice: str = "zh-CN-YunyangNeural") -> str:
    import asyncio
    import os
    from edge_tts import Communicate

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "..", "tempfile")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, "output_audio.mp3")

    # 创建新的事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(text_to_speech(text, voice, output_file))
    finally:
        loop.close()

    return output_file



# 使用示例
if __name__ == "__main__":
    TEXT = """分析：**上海工程技术大学松江校区图书馆**的建筑风格与图片主特征最相近，特征为：这些建筑具有独特的几何形状，主要由三角形和多边形构成，并且建筑物的外观设计独特，部分区域有玻璃幕墙。由此可知，该图书馆的建筑设计风格符合图片中的描述。而**上海视觉艺术学院设计楼**的建筑风格虽然也具有几何形状，但更侧重于简洁的线条和开放式露台设计，因此与图片中的描述并不完全一致。**上海工程技术大学松江校区现代工业工程训练中心**的建筑风格较为简洁，线条清晰，与图片中的独特几何形状特征有一定差距，因此也不是最接近的地点。

**上海工程技术大学松江校区图书馆**为最相似的地点。"""

    # 生成音频并获取输出文件路径
    audio_path = generate_audio(TEXT)  # 调用生成音频函数
    print(f"音频文件保存路径: {audio_path}")  # 打印生成的音频文件路径
