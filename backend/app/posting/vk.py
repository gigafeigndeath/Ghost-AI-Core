from app.config import settings
import vk_api

vk_session = vk_api.VkApi(token=settings.VK_API_TOKEN)
vk = vk_session.get_api()

def post_to_vk(content: str, image_url: str = None, schedule_time: str = None):
    # Упрощено
    vk.wall.post(message=content, attachments=image_url)
    return "Posted to VK"