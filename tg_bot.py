import re

import telebot

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

    print("Ready")
    bot.infinity_polling()
