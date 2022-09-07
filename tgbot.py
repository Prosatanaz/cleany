import telebot
import re
from order_service import *

bot = telebot.TeleBot('5612156914:AAEiFzNR0KVrvYDE7OjnSbjiKJrtPCwW_N8')


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        
        msg =  bot.send_message(message.chat.id,"hi", reply_markup=generate_calc_keyboard())
        form_list_to_send(message.chat.id, msg)

    elif message.text == '/calendar':
       calendar, step = DetailedTelegramCalendar().build()

       bot.send_message(message.chat.id,f'Select {LSTEP[step]}',reply_markup=calendar)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)
    user_id = call.message.chat.id
    user_answer = call.data

    if re.match(f"[+-]{BUTTON_VALUE_SEPARATOR}\d+", user_answer):
        add_remove_buttons_handler(user_id=user_id, user_answer=user_answer)
    elif user_answer == "cancel":
        cancel_order(bot, user_id)


print("Ready")
bot.infinity_polling()
