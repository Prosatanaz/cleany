from telebot import TeleBot
from datetime import date
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

bot = TeleBot("5485478360:AAGsfep09KeFIEMXiSYFZ4g8Cs0TAOJeE3o")
admin_id = 0

def generate_admin_keyboard():
    markup = InlineKeyboardMarkup()
    amount_orders_button = InlineKeyboardButton('показать количество заказов', callback_data='amount_orders')
    markup.row(amount_orders_button)
    return markup

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/admin_panel':
      
      
        write_password(message.chat.id)

        
def write_password(id):
    next_step =  bot.send_message(id, "введите пароль")
    bot.register_next_step_handler(next_step, init_logging)
    


def init_logging(message):
    if message.text == 'ZYZZ112233':
        global admin_id
        bot.send_message(message.chat.id, 'вы вошли в панель администратора, выберите действие:', reply_markup=generate_admin_keyboard())
        admin_id = message.chat.id
        
    else:    
        next_step =  bot.send_message(message.chat.id, 'неправильный пароль \n попробуйте еще раз')
        bot.register_next_step_handler(next_step, init_logging)

bot.polling()        

