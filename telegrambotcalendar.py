from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_calendar.base import DAY
from telegram_bot_calendar.detailed import DetailedTelegramCalendar

bot = TeleBot("5485478360:AAGsfep09KeFIEMXiSYFZ4g8Cs0TAOJeE3o")

SEPARATOR_BUTTON = ':'


class WMonthTelegramCalendar(DetailedTelegramCalendar):
    first_step = DAY


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        calendar, step = WMonthTelegramCalendar(locale='ru').build()

        bot.send_message(message.chat.id, "выберите дату заказа", reply_markup=calendar)


@bot.callback_query_handler(func=WMonthTelegramCalendar.func())
def cal(c):
    result, key, step = WMonthTelegramCalendar().process(c.data)

    if not result and key:
        bot.edit_message_text("выберите дату заказа", c.message.chat.id, c.message.message_id, reply_markup=key)
    elif result:
        bot.edit_message_text("Выберите время заказа", c.message.chat.id, c.message.message_id,
                              reply_markup=draw_clock_keyboard(result))


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, )
    check_time(call)


def check_time(call):
    if call.data == call.data:
        print(call.data)
        return call.data


def draw_clock_keyboard(result):
    clock_markup = InlineKeyboardMarkup()

    for hour in range(9, 19):
        draw_clock_buttons(clock_markup, hour, result)

    return clock_markup

def draw_clock_buttons(keyboard, hour,result):

    full_time_button = InlineKeyboardButton(str(hour) + SEPARATOR_BUTTON +'00',callback_data= str(result) + '-' + str(hour) + SEPARATOR_BUTTON +'00')
    if hour !=18:
        half_time_button = InlineKeyboardButton(str(hour) + SEPARATOR_BUTTON +'30',callback_data=str(result) + '-' +  str(hour) + SEPARATOR_BUTTON +'30')
        keyboard.row(full_time_button, half_time_button)
    else:
        keyboard.row(full_time_button)
    return keyboard


print('rdy')
bot.polling()
