import asyncio
import edge_tts
import os


async def text_to_speech(text: str, voice: str, output_file: str) -> None:
    """将文本转换为语音并保存为音频文件。"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


def generate_audio(text: str, voice: str = "zh-CN-YunyangNeural") -> str:
    """
    将文本转换为语音并保存为音频文件，输出到相邻的 tempfile 目录。

    参数:
    - text: 要转换为语音的文本。
    - voice: 使用的语音模型（默认为 'zh-CN-YunyangNeural'）。

    返回值:
    - 生成的音频文件的路径。
    """
    # 1.获取当前代码所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在的绝对路径

    # 2.指定音频文件保存到 tempfile 目录
    output_dir = os.path.join(current_dir, "..", "tempfile")  # 生成 tempfile 目录的路径（与 tts 目录同级）

    # 3.确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 如果目录不存在，则创建目录

    # 4.基于文本或生成随机文件名
    output_file = os.path.join(output_dir, "output_audio.mp3")  # 保存的文件名为 output_audio.mp3

    # 5.运行异步->文本到语音转换函数
    loop = asyncio.get_event_loop_policy().get_event_loop()  # 获取事件循环
    try:
        loop.run_until_complete(text_to_speech(text, voice, output_file))  # 运行异步任务，生成音频
    finally:
        loop.close()  # 关闭事件循环

    return output_file  # 返回生成的音频文件路径


# 使用示例
if __name__ == "__main__":
    TEXT = "分析：上海工程技术大学松江校区图书馆的建筑风格与图片主特征最相近，特征为：具有独特的几何形状，主要以三角形和多边形为主，设计现代且具有未来感。由此可知，该地点的建筑风格与图片中的描述高度一致。而上海视觉艺术学院设计楼的建筑风格虽然现代化，但更侧重于简洁的线条和大面积的玻璃窗，并不完全符合图片中提到的独特几何形状的特点；上海工程技术大学松江校区体育馆则更多地采用了金属结构和呈现波浪形或弧形的屋顶设计，这些特征与图片中的描述也有一定差异。因此，上海工程技术大学松江校区图书馆为最相似的地点。"

    # 生成音频并获取输出文件路径
    audio_path = generate_audio(TEXT)  # 调用生成音频函数
    print(f"音频文件保存路径: {audio_path}")  # 打印生成的音频文件路径
