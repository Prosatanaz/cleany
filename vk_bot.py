import glob
import json
import os

import gspread
import vk_api
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

def return_start_point_vk():
    return 'VK'
    
def start_vk_bot():
    print('Start VK Bot')
    GROUP_ID = '215429808'
    GROUP_TOKEN = 'vk1.a.-OoF4Nyf_mvkHPLzJA4X_1npTgwmNNartyqUQAPculjCrmjUmjUgw9-IaJEomxOq3xuwqwvkRJHRPLaagmJPPx1O8AG9NSftAa0mgfPKkKOaJxfzdcS35IJhHdG3P4dy4yw7ak_h9bGuQkHkE2_3xq2G5dffG_q74AO-pcEbI9ISrXp2frwCfFOD314Blz1d'
    API_VERSION = '5.130'

    HI = []
    HI.append("start")
    HI.append("Start")
    HI.append("начать")
    HI.append("Начало")
    HI.append("Начать")
    HI.append("начало")
    HI.append("Бот")
    HI.append("бот")
    HI.append("Старт")
    HI.append("старт")
    HI.append('Запустить бота!')

    vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

    settings = dict(one_time=False, inline=False)
    keyboard_start = VkKeyboard(**settings)
    keyboard_start.add_button(label='Запустить бота!', color=VkKeyboardColor.POSITIVE, payload={"type": "Старт"})

    holder_path = os.path.abspath(__file__).rpartition("\\")[0]
    gc = gspread.service_account(f"{holder_path}\clinny-361618-f313b3437739.json")
    worksheet = gc.open_by_url(
       "https://docs.google.com/spreadsheets/d/115gY9pcQghGnjV5FLfnDZELuTu6invP72rK40sb3em8/edit#gid=0")


    def get_base_clean_info():
        clean_info = worksheet.get_worksheet(1).get_all_values()
        clean_zones = []
        clean_zones_description = []
        for i in clean_info:
            clean_zones.append(i[0])
            clean_zones_description.append(i[1])

        return clean_zones, clean_zones_description


    def get_cleaners_info():
        cleaners_info = worksheet.get_worksheet(0).get_all_values()[1:]
        names = []
        photos = []
        experiences = []
        descriptions = []
        for i in cleaners_info:
            names.append(i[0])
            photos.append(i[1])
            experiences.append(i[2])
            descriptions.append(i[3])

        return  cleaners_info

    cleaners_info = get_cleaners_info()

    def generate_main_keyboard():
        settings = dict(one_time=False, inline=False)
        keyboard_menu = VkKeyboard(**settings)
        keyboard_menu.add_button(label="Базовая уборка", color=VkKeyboardColor.SECONDARY)
        keyboard_menu.add_line()
        keyboard_menu.add_button(label="Наши работницы", color=VkKeyboardColor.SECONDARY)
        keyboard_menu.add_line()
        keyboard_menu.add_callback_button(label="Контакты администратора", color=VkKeyboardColor.SECONDARY, payload={"type": "open_link", "link": "https://rt.pornhub.com/pornstar/johnny-sins"})
        keyboard_menu.add_line()
        keyboard_menu.add_callback_button(label="Мы в телеграм!", color=VkKeyboardColor.SECONDARY, payload={"type": "open_link", "link": "https://t.me/cleanytestbot"})
        keyboard_menu.add_line()
        keyboard_menu.add_callback_button(label="Отзывы о нашей работе", color=VkKeyboardColor.SECONDARY, payload={"type": "reviews"})
        return keyboard_menu

    main_keyboard = generate_main_keyboard()

    def generate_base_clean_keyboard():
        settings = dict(one_time=False, inline=False)
        keyboard_clean_zones = VkKeyboard(**settings)
        clean_zones, T = get_base_clean_info()
        for i in clean_zones:
            keyboard_clean_zones.add_callback_button(label=i, color=VkKeyboardColor.SECONDARY,
                                            payload={"type": f"${i}"})
            keyboard_clean_zones.add_line()

        keyboard_clean_zones.add_callback_button(label="Назад к меню", color=VkKeyboardColor.PRIMARY, payload={"type": "back_menu"})
        return  keyboard_clean_zones

    def generate_cleaners_markup():
        settings = dict(one_time=False, inline=False)
        keyboard_cleaners = VkKeyboard(**settings)
        for i in cleaners_info:
            print(i[0])
            keyboard_cleaners.add_callback_button(label=i[0], color=VkKeyboardColor.SECONDARY, payload={"type": f"%{i[0]}"})
            keyboard_cleaners.add_line()

        keyboard_cleaners.add_callback_button(label="Назад к меню", color=VkKeyboardColor.PRIMARY,
                                                 payload={"type": "back_menu"})
        return keyboard_cleaners


    def send_reviews(event):
        upload = vk_api.VkUpload(vk)
        for i in glob.glob("reviews\*.png"):
            photo = upload.photo_messages(i)
            owner_id = photo[0]['owner_id']
            photo_id = photo[0]['id']
            access_key = photo[0]['access_key']
            attachment = f'photo{owner_id}_{photo_id}_{access_key}'
            vk.messages.send(peer_id=event.object.peer_id, random_id=0, attachment=attachment)



    def get_base_clean_descr(zone):
        clean_zones, clean_zones_description = get_base_clean_info()
        for i in range(len(clean_zones)):
            if clean_zones[i] == zone:
                return clean_zones_description[i]

    def get_cleaner_description(name):
        cleaner_info = []
        for i in cleaners_info:
            if i[0] == name:
                cleaner_info = i
                break

        experience = i[2]
        description = i[3]
        upload = vk_api.VkUpload(vk)
        photo = upload.photo_messages(f'{i[1]}')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        return experience, description, attachment


    def send_message(event, text, keyboard):
        if keyboard == None:
            vk.messages.send(
                user_id=event.obj.message['from_id'],
                random_id=get_random_id(),
                peer_id=event.obj.message['from_id'],
                message=text)
        else:
            vk.messages.send(
            user_id=event.obj.message['from_id'],
            random_id=get_random_id(),
            peer_id=event.obj.message['from_id'],
            keyboard = keyboard.get_keyboard(),
            message=text)



    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:

            if event.obj.message['text'] != '':

                if event.from_user:
                    if event.obj.message["text"] in HI:
                        send_message(event, "Вас приветствует бот cleanny.by!", main_keyboard)

                    elif event.obj.message["text"] == "Базовая уборка":
                        send_message(event, "Здесь вы можете посмотреть, что входит в базовую уборку:", generate_base_clean_keyboard())

                    elif event.obj.message["text"] == "Наши работницы":
                        send_message(event, "Наши работницы: ", generate_cleaners_markup())

                    elif event.obj.message["text"] == "Контакты администратора":
                        send_message(event, "Контакты администратора", None)

                    elif event.obj.message["text"] == "Мы в телеграм!":
                        send_message(event, "Мы в телеграм!", None)



        elif event.type == VkBotEventType.MESSAGE_EVENT:
            CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app', 'text')
            flag = event.object.payload.get('type')[0]
            data = event.object.payload.get('type')[1:]

            if event.object.payload.get('type') in CALLBACK_TYPES:
                vk.messages.sendMessageEventAnswer(
                    event_id=event.object.event_id,
                    user_id=event.object.user_id,
                    peer_id=event.object.peer_id,
                    event_data=json.dumps(event.object.payload))

            if flag == "$":
                msg = get_base_clean_descr(data)
                vk.messages.send(
                    event_id=event.object.event_id,
                    random_id=get_random_id(),
                    user_id=event.object.user_id,
                    peer_id=event.object.peer_id,
                    event_data=json.dumps(event.object.payload),
                    message=f"{data}:\n{msg}")

            if flag == "%":
                experience, description, attachment = get_cleaner_description(data)
                vk.messages.send(peer_id=event.object.peer_id, random_id=0, attachment=attachment)
                vk.messages.send(
                    event_id=event.object.event_id,
                    random_id=get_random_id(),
                    user_id=event.object.user_id,
                    peer_id=event.object.peer_id,
                    keyboard=generate_cleaners_markup().get_keyboard(),
                    message=f"{experience}\n{description}")

            if event.object.payload.get("type")  == "reviews":
                send_reviews(event)

            if event.object.payload.get("type") == "back_menu":
                vk.messages.send(
                    event_id=event.object.event_id,
                    random_id=get_random_id(),
                    user_id=event.object.user_id,
                    peer_id=event.object.peer_id,
                    keyboard=main_keyboard.get_keyboard(),
                    message="Вас приветствует cleanny.by!")
