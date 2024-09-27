import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse, urlencode
import ssl
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
import websocket

# 定义API凭证变量
appid = "xxxxxxxx"  # APPID
api_secret = "xxxxxxxxxxxx"  # APISecret
api_key = "xxxxxxxxxxxxxxxxxx"  # APIKey
imagedata = open("SUES03.png", 'rb').read()  # 打开并读取图片文件

# 设置图像理解服务的WebSocket URL
imageunderstanding_url = "wss://spark-api.cn-huabei-1.xf-yun.com/v2.1/image"
# 将图像数据编码为base64格式
image_base64 = str(base64.b64encode(imagedata), 'utf-8')

class Ws_Param:
    """用于管理WebSocket连接参数的类"""
    def __init__(self, appid, api_key, api_secret, imageunderstanding_url):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.host = urlparse(imageunderstanding_url).netloc  # 解析URL获取主机名
        self.path = urlparse(imageunderstanding_url).path  # 解析URL获取路径
        self.image_understanding_url = imageunderstanding_url

    def create_url(self):
        """创建带有认证信息的URL"""
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))  # 获取格式化的时间
        signature_origin = f"host: {self.host}\ndate: {date}\nGET {self.path} HTTP/1.1"
        signature_sha = hmac.new(self.api_secret.encode('utf-8'), signature_origin.encode('utf-8'), hashlib.sha256).digest()  # HMAC-SHA256签名
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')  # 对签名进行Base64编码
        authorization_origin = (f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", '
                                f'signature="{signature_sha_base64}"')
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')  # 对整个授权头进行Base64编码
        auth_params = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        return self.image_understanding_url + '?' + urlencode(auth_params)  # 创建完整的URL

class WebSocketHandler:
    """用于处理WebSocket通信的类"""
    def __init__(self, appid, messages):
        self.appid = appid
        self.messages = messages
        self.answer = ""

    def on_error(self, ws, error):
        """WebSocket发生错误时调用"""
        print("错误:", error)

    def on_close(self, ws, one=None, two=None):
        """WebSocket关闭时调用"""
        print("\n连接已关闭")

    def on_open(self, ws):
        """WebSocket连接成功开启时调用"""
        thread.start_new_thread(self.run, (ws,))

    def run(self, ws):
        """在WebSocket连接开启后执行发送消息的操作"""
        data = json.dumps(self.gen_params(self.appid, self.messages))
        ws.send(data)

    def on_message(self, ws, message):
        """接收到WebSocket消息时调用"""
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            print(f'请求错误: {code}, {data}')
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            print(content, end="")
            self.answer += content
            if status == 2:
                ws.close()

    @staticmethod
    def gen_params(appid, messages):
        """生成WebSocket请求的参数"""
        return {
            "header": {
                "app_id": appid
            },
            "parameter": {
                "chat": {
                    "domain": "image",
                    "temperature": 0.5,
                    "top_k": 4,
                    "max_tokens": 2028,
                    "auditing": "default"
                }
            },
            "payload": {
                "message": {
                    "text": messages
                }
            }
        }

def start_websocket(appid, api_key, api_secret, imageunderstanding_url, messages):
    """初始化并启动WebSocket连接"""
    ws_param = Ws_Param(appid, api_key, api_secret, imageunderstanding_url)  # 创建参数对象
    websocket.enableTrace(False)  # 禁用WebSocket调试输出
    ws_url = ws_param.create_url()  # 获取完整的WebSocket URL

    ws_handler = WebSocketHandler(appid, messages)  # 创建WebSocket处理器
    ws = websocket.WebSocketApp(ws_url,
                                on_message=ws_handler.on_message,
                                on_error=ws_handler.on_error,
                                on_close=ws_handler.on_close,
                                on_open=ws_handler.on_open)
    ws.appid = appid
    ws.messages = messages
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})  # 启动WebSocket，使用不验证证书的SSL选项

if __name__ == '__main__':
    prompt = """
请对提供的图像进行分析，关注以下要点：

1. **设计风格**：
   - 描述建筑或风景的主要设计特点。
   - 讨论其可能的文化或历史联系。

2. **具体特征与位置关系**：
   - 描述图像中显著事物的特征。
   - 推测其可能的地理位置。

3. **环境描述**：
   - 描述自然与人造元素。
   - 分析这些元素如何影响场景。

4. **文字与标志**：
   - 描述可见的文字或标志。
   - 推测其含义。

5. **人物活动**：
   - 描述人物的活动。
   - 分析其与环境的关系。

请直接、简洁地回答，避免不必要的修饰。
"""

    # 将图像数据和提示组合成消息列表
    messages = [
        {"role": "user", "content": image_base64, "content_type": "image"},
        {"role": "user", "content": prompt, "content_type": "text"}
    ]
    print("回答:", end="")
    start_websocket(appid, api_key, api_secret, imageunderstanding_url, messages)  # 启动WebSocket并发送消息
