from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from site_parser import Parser

bot = TeleBot('5485478360:AAGsfep09KeFIEMXiSYFZ4g8Cs0TAOJeE3o')
last_bot_message = 0
parser = Parser()
servise_names, servise_description = parser.get_standart_clean_info()

return_main_markup_button = InlineKeyboardButton('Главное меню', callback_data='menu')
main_menu_markup = InlineKeyboardMarkup(row_width=2)
service_button_description = InlineKeyboardButton('Базовые услуги', callback_data='service')
reviews_button = InlineKeyboardButton('Отзывы', call_data='reviews')
main_menu_markup.row(service_button_description, reviews_button)


# TODO make description
def edit_service_descridption(user_Id, msg_id):
    pass


def edit_to_main_menu(chat_id, msg_id):
    bot.edit_message_text('главное меню', chat_id, msg_id)


# TODO make reviews
def edit_reviews(chat_id, msg_id):
    pass


# TODO make cleaners description
def edit_cleaners_description(chat_id, msg_id):
    pass


@bot.message_handler(content_types=['text'])
def start(message):
    global last_bot_message
    if message.text == '/start':
        last_bot_message = bot.send_message(message.chat.id, 'главное меню', reply_markup=main_menu_markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global last_bot_message
    bot.answer_callback_query(callback_query_id=call.id)
    user_id = call.message.chat.id
    user_answer = call.data
    if call.data == 'service':
        edit_service_descridption(user_id, last_bot_message)

    elif call.data == 'reviews':
        edit_reviews(user_id, last_bot_message)

    elif call.data == 'menu':
        edit_to_main_menu(user_id, last_bot_message)

    elif call.data == 'cleaners':
        edit_cleaners_description(user_id, last_bot_message)
