import json

def extract_snippets(data):
    snippets = []
    idx = 1
    for message in data.get('messages', []):
        if message['type'] == 'source' and message['content_type'] in ('webpage', 'text', 'douyin'):
            try:
                content = json.loads(message.get('content', '{}'))
                if 'value' in content:
                    for item in content['value']:
                        snippet = item.get('snippet')
                        if snippet:
                            snippets.append(f"{idx}. {snippet}")
                            idx += 1
                if 'videos' in content:
                    for video in content['videos']:
                        snippet = video.get('description')
                        if snippet:
                            snippets.append(f"{idx}. {snippet}")
                            idx += 1
            except json.JSONDecodeError:
                continue
    return snippets

def extract_urls(data):
    urls = []
    idx = 1
    for message in data.get('messages', []):
        if message['type'] == 'source' and message['content_type'] in ('webpage', 'text', 'douyin'):
            try:
                content = json.loads(message.get('content', '{}'))
                if 'value' in content:
                    for item in content['value']:
                        if 'url' in item and item['url'] not in urls:
                            urls.append(f"{idx}. {item['url']}")
                            idx += 1
                            if len(urls) == 6:
                                return urls
                        if 'contentUrl' in item and item['contentUrl'] not in urls:
                            urls.append(f"{idx}. {item['contentUrl']}")
                            idx += 1
                            if len(urls) == 6:
                                return urls
                        if 'thumbnailUrl' in item and item['thumbnailUrl'] not in urls:
                            urls.append(f"{idx}. {item['thumbnailUrl']}")
                            idx += 1
                            if len(urls) == 6:
                                return urls
                if 'videos' in content:
                    for video in content['videos']:
                        content_url = video.get('content_url')
                        if content_url and content_url not in urls:
                            urls.append(f"{idx}. {content_url}")
                            idx += 1
                            if len(urls) == 6:
                                return urls
                        for image in video.get('cover_images', []):
                            image_url = image.get('url')
                            if image_url and image_url not in urls:
                                urls.append(f"{idx}. {image_url}")
                                idx += 1
                                if len(urls) == 6:
                                    return urls
            except json.JSONDecodeError:
                continue
    return urls
