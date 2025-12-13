from .telegram import post_to_telegram
from .vk import post_to_vk

def get_poster(platform: str):
    if platform == "telegram":
        return post_to_telegram
    elif platform == "vk":
        return post_to_vk
    else:
        raise ValueError("Unknown platform")

def post_to_platform(platform: str, content: str, image_url: str = None, schedule_time: str = None):
    poster = get_poster(platform)
    return poster(content, image_url, schedule_time)