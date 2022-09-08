
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import tg_messenger

bot = TeleBot("5485478360:AAGsfep09KeFIEMXiSYFZ4g8Cs0TAOJeE3o")
def generate_check_number_markup():

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('да', callback_data='да'),
                        InlineKeyboardButton('нет', callback_data='нет'))
    return markup
def generate_check_adress_markup():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('да', callback_data='да1'),
                        InlineKeyboardButton('нет', callback_data='нет1'))
    return markup

    #прикрути кнопку следуюшего щага
if call.data == 'кнопка':
        print(message.chat.id)
        write_number(message.chat.id)


def write_number(id):
    next_step = bot.send_message(id, "введите контактный номер телефона")
    bot.register_next_step_handler(next_step, check_number)


def check_number(message):
    bot.send_message(message.chat.id, ' это ваш телефон? ', reply_markup=generate_check_number_markup())



def write_adress(id):
    next_step = bot.send_message(id, "введите адрес")
    bot.register_next_step_handler(next_step, check_adress)


def check_adress(message):
   
    next_step = bot.send_message(message.chat.id, ' это ваш адрес? ', reply_markup=generate_check_adress_markup())







def payment_metod(id):
    bot.send_message(id, 'выберите способ оплаты',reply_markup=generate_payment_markup(id))
from order import Order,
from payment_manager import paymentManager
def generate_payment_markup(id,order):
    #заглушка
    order = Order()
    #заглушка
    datatime = order.datatime
    price = order.get_total_price()

    pay_url = paymentManager().get_pay_url(price, str(id), datatime )
    markup = InlineKeyboardMarkup()
    cash_button = InlineKeyboardButton('оплата наличными', callback_data='cash')
    card_button = InlineKeyboardButton('оплата картой',callback_data='card')
    online_button = InlineKeyboardButton('оплатить онлайн',url=pay_url,callback_data='online')
    markup.row(cash_button,card_button)
    markup.row(online_button)
    return markup





@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, )
    if call.data == 'да':
        write_adress(call.message.chat.id)
        #положить number в order
    elif call.data == 'нет':
        write_number(call.message.chat.id)
    elif call.data == 'да1':
        #нужно положить adress в order
        payment_metod(call.message.chat.id)
    elif call.data == 'нет1':
        write_adress(call.message.chat.id)
    elif call.data == 'cash':
        #положить cash  В  order payment_metod 
    elif call.data == 'card':
        #положить card  В  order payment_metod
    elif call.data == 'online':
        #положить online в order  payment_metod 
        #добавить статус оплаты     

             


print('rdy')
bot.polling()
