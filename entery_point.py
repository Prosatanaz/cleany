from tgbot import start_tg_bot, return_start_point_tg
from Vkcleanny import return_start_point_vk, start_vk_bot


BOT_TYPES = [return_start_point_tg(),return_start_point_vk()]

TG_BOT = "TG"
VK_BOT = "VK"
INSTAGRAM_BOT = "IG"
WHATSAPP_BOT = "WA"
for BOT_TYPE in BOT_TYPES:
    if BOT_TYPE == TG_BOT:
        start_tg_bot()
    elif BOT_TYPE == VK_BOT:
        start_vk_bot()
    elif BOT_TYPE == INSTAGRAM_BOT:
        pass
    elif BOT_TYPE == WHATSAPP_BOT:
        pass

