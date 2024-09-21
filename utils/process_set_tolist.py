"""
1.将set集合数据转为list集合数据
"""


def convert_sets_to_lists(obj):
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, list):
        return [convert_sets_to_lists(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_sets_to_lists(value) for key, value in obj.items()}
    else:
        return obj
