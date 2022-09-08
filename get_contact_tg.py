from multiprocessing.forkserver import set_forkserver_preload
from time import time
from telebot import TeleBot
from datetime import date
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

bot = TeleBot("5485478360:AAGsfep09KeFIEMXiSYFZ4g8Cs0TAOJeE3o")

markup_check_number = InlineKeyboardMarkup()
markup_check_number.row(InlineKeyboardButton('да',callback_data= 'да'), InlineKeyboardButton ('нет', callback_data= 'нет'))


markup_check_adress = InlineKeyboardMarkup()
markup_check_adress.row(InlineKeyboardButton('да',callback_data= 'да1'), InlineKeyboardButton ('нет', callback_data= 'нет1'))

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        print(message.chat.id)
        write_number(message.chat.id)
        
        
       
def write_number(id):
    next_step =  bot.send_message(id, "введите контактный номер телефона")
    bot.register_next_step_handler(next_step,check_number)

def check_number(message):
    next_step = bot.send_message(message.chat.id, ' это ваш телефон? ', reply_markup=markup_check_number)
    

#нужно положить number в order
def confirm_number(message):
    if message.text == 'да':
        
        bot.register_next_step_handler(message, write_adress)
    elif message.text =='нет':
        bot.register_next_step_handler(message, write_number)    

def write_adress(id):
    next_step =  bot.send_message(id, "введите адрес")
    bot.register_next_step_handler(next_step, check_adress)

def check_adress(message):
    next_step = bot.send_message(message.chat.id, ' это ваш адрес? ',reply_markup= markup_check_adress)

    
#нужно положить adress в order
def confirm_adres(message):
    if message.text == 'да':
        bot.register_next_step_handler(message.text,poel_govna)
    elif message.text =='нет':
        bot.register_next_step_handler(message.text, write_adress)  

#конечный метод        
def poel_govna():
    pass

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id,)
    if call.data == 'да':
        write_adress(call.message.chat.id)
    if call.data == 'нет':
        write_number(call.message.chat.id)
    if call.data == 'да1':
        write_adress(call.message.chat.id)
    if call.data == 'нет1':
        write_number(call.message.chat.id)
             

print('rdy')
bot.polling()



                           


  
