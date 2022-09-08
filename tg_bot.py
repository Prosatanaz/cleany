import glob
import re

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

import sheets_reader
from services import ServicesManager
from tg_messenger import BUTTON_VALUE_SEPARATOR
from tg_messenger import TgMessenger
from tg_order_service import *

def return_start_point_tg():
    return 'TG'
def start_tg_bot():
    print("start bot for Telegram")
    bot = telebot.TeleBot('5612156914:AAEiFzNR0KVrvYDE7OjnSbjiKJrtPCwW_N8')
    messenger = TgMessenger(bot)

    main_menu_markup = InlineKeyboardMarkup()
    main_menu_markup.add(InlineKeyboardButton('Базовые услуги', callback_data='service'))
    main_menu_markup.add(InlineKeyboardButton('Отзывы', callback_data='reviews'))
    main_menu_markup.add(InlineKeyboardButton('Наши работницы', callback_data='cleaners'))

    @bot.message_handler(content_types=['text'])
    def start(message):
        user_id = message.chat.id
        if message.text == '/start':
            messenger.send_start(user_id)

    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        bot.answer_callback_query(callback_query_id=call.id)
        user_id = call.message.chat.id
        message_id = call.message.message_id
        callback_data = call.data
        flag = callback_data[0]
        data = callback_data[1:]

        if callback_data == "order_new":
            ServicesManager.set_basic_service(tabel=sheets_reader.get_basic_service_data())
            ServicesManager.set_extra_services(tabel=sheets_reader.get_extra_services_data())
            message_id = messenger.send_basic_service(user_id)
            create_order(user_id, message_id)

        elif re.match(f"[+-]{BUTTON_VALUE_SEPARATOR}\d+", callback_data):
            add_remove_extra_service_buttons_handler(user_id=user_id, callback_data=callback_data)
            order = OrdersManager.get_order(user_id)
            messenger.edit_to_extra_services(order)

        elif callback_data == "continue":
            continue_button_handler(user_id)

        elif callback_data == "return":
            return_button_handler(user_id)

        elif callback_data == "cancel":
            messenger.delete_message(user_id, message_id)
            delete_order(user_id)

        elif callback_data == "menu":
            bot.send_message(user_id, "Здесь вы можете узнать подробности нашей работы", reply_markup=main_menu_markup)

        elif callback_data == "go_menu":
            messenger.send_start(user_id)

        elif callback_data == "service":
            bot.send_message(user_id, "В базовую стоимость уборки входит", reply_markup=generate_base_clean_markup())

        elif callback_data == "reviews":
            send_reviews(user_id)

        elif callback_data == "cleaners":
            bot.send_message(user_id, "Наши работницы", reply_markup=generate_cleaners_markup())

        if flag == "#":
            send_cleaner_descr(data, user_id)

        if flag == "$":
            send_base_clean_description(data, user_id)

    def continue_button_handler(user_id):
        order = OrdersManager.get_order(user_id)
        print(f"order_stage - {order.stage.name}")
        messenger.edit_to_stage(order, order.get_next_stage())

    def return_button_handler(user_id):
        order = OrdersManager.get_order(user_id)
        messenger.edit_to_stage(order, order.get_previous_stage())

    def add_remove_extra_service_buttons_handler(user_id, callback_data):
        # callback consists of 2 parts - is needed to add or remove service and service id
        splitted_user_answer = callback_data.split(BUTTON_VALUE_SEPARATOR)
        is_add = splitted_user_answer[0] == "+"
        service_id = splitted_user_answer[1]

        order = OrdersManager.get_order(user_id)
        service = ServicesManager.get_service(service_id)

        if is_add:
            order.add_service(service)
        else:
            order.remove_service(service)

    def send_reviews(id):
        reviews_input_list = []
        for i in glob.glob("reviews\*.png"):
            review = open(i, "rb")
            reviews_input_list.append(InputMediaPhoto(review))

        bot.send_media_group(id, reviews_input_list)
        messenger.send_start(id)

    def generate_base_clean_markup():
        base_info_markup = InlineKeyboardMarkup()
        base_zones, T = sheets_reader.get_base_clean_info()
        for i in base_zones:
            base_info_markup.add(InlineKeyboardButton(i, callback_data=f"${i}"))

        base_info_markup.add(InlineKeyboardButton("Назад в меню", callback_data="go_menu"))
        return base_info_markup

    def send_base_clean_description(zone, id):
        base_zones, base_zones_desc = sheets_reader.get_base_clean_info()
        for i in range(len(base_zones)):
            if base_zones[i] == zone:
                bot.send_message(id, base_zones_desc[i])

        bot.send_message(id, "В базовую стоимость уборки входит", reply_markup=generate_base_clean_markup())

    def generate_cleaners_markup():
        cleaners_info = sheets_reader.get_cleaners_info()
        cleaners_markup = InlineKeyboardMarkup()
        for i in cleaners_info:
            cleaners_markup.add(InlineKeyboardButton(i[0], callback_data=f"#{i[0]}"))

        cleaners_markup.add(InlineKeyboardButton("Назад в меню", callback_data="go_menu"))
        return cleaners_markup

    def send_cleaner_descr(name, id):
        cleaners_info = sheets_reader.get_cleaners_info()
        for i in cleaners_info:
            if i[0] == name:
                bot.send_message(id, i[2])
                photo = open(i[1], "rb")
                bot.send_photo(id, photo=photo)
                photo.close()
                bot.send_message(id, i[3])
                break

        bot.send_message(id, "Наши работницы", reply_markup=generate_cleaners_markup())

    print("Ready")
    bot.infinity_polling()
