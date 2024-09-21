import base64
import requests

# 1.读取图像
def encode_image(file_path_or_url):
    try:
        if file_path_or_url.startswith('http'):
            response = requests.get(file_path_or_url)
            image_data = response.content
        else:
            with open(file_path_or_url, "rb") as image_file:
                image_data = image_file.read()
        return base64.b64encode(image_data).decode('ascii')
    except Exception as e:
        print(f"Error processing the image: {e}")
        return None

