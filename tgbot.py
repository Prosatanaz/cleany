from calendar import calendar
from sys import call_tracing, exec_prefix
import time
from typing import Literal
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
import gspread
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

orders = []
bot = telebot.TeleBot('5600966956:AAF-YStSKMZnF9aOEGKAPRdNFffTCYEya8s')
gc = gspread.service_account(filename="clinny-361618-f313b3437739.json")
calc_sheet_url = gc.open_by_url('https://docs.google.com/spreadsheets/d/115gY9pcQghGnjV5FLfnDZELuTu6invP72rK40sb3em8/edit#gid=480424214')
worksheet_calc = calc_sheet_url.get_worksheet(4)
data_from_sheet = worksheet_calc.get_all_values()
print(data_from_sheet)


def generate_calc_keyboard():
    markup_servise = InlineKeyboardMarkup()
    list_of_service = data_from_sheet[0]
    counter = 2
    for service in list_of_service[2::]:
        btn1 = InlineKeyboardButton(service, callback_data='g' + str(counter))
        btn2 = InlineKeyboardButton('+',callback_data= '+'+str(counter) )
        btn3 =  InlineKeyboardButton('-',callback_data= '-'+str(counter))
        markup_servise.row(btn1)
        markup_servise.row(btn2, btn3)
        counter += 1
    return markup_servise

def form_list_to_send(id, msg):
    global orders
    list_of_servise_to_user = []
    list_of_time_for_user = []
    list_of_price_for_user = []
    message_id = msg.message_id
    order = []
    order.append(id)
    order.append(list_of_servise_to_user)
    order.append(list_of_time_for_user)
    order.append(list_of_price_for_user)
    order.append(message_id)
    orders.append(order)
    print(orders)
    
  

def add_servise_for_user(number_of_servise,id):
    print("ggggg")
    global orders
    for order in orders:
        if id == order[0]:
            current_order = order
            
 
    service_list =  data_from_sheet[3]
    price_list = data_from_sheet[1]
    time_list = data_from_sheet[2]

    current_order[1].append(service_list[number_of_servise])
    current_order[2].append(time_list[number_of_servise])
    current_order[3].append(price_list[number_of_servise])
   
    return(current_order)
        
def edit_message(current_order):
    service =  current_order[1]
    all_time = current_order[2]
    all_prices = current_order[3]
  
    for service_name in service:
        string_servise = 'дополнительные  услуги:  ' + service_name + '\n'
    print(string_servise)
    for cleaning_time in all_time:
        total_time = float(cleaning_time)
     
        
    string_time = 'приблизительное время уборки:    ' + str(total_time) + '\n'   

    for price in all_prices:
        total_price = price
       
    string_price = 'стоймость уборки' + str(total_price)
    
    text_to_edit = string_time + string_price
    print(text_to_edit)   
    bot.edit_message_text(text_to_edit, current_order[0], current_order[4], reply_markup=generate_calc_keyboard())
   




   

def remove_servise_for_user(number_of_servise, id):
    global orders
    for order in orders:
        if id == order[0]:
            current_order = order
            
 
    service_list =  data_from_sheet[3]
    price_list = data_from_sheet[1]
    time_list = data_from_sheet[2]

    try:
        current_order[1].remove(service_list[number_of_servise])
        current_order[2].remove(time_list[number_of_servise])
        current_order[3].remove(price_list[number_of_servise])
    except:
        pass
    return(current_order)
def send_info_to_user(list_for_send_to_user):
    True

    
def dt(s):
    s = s[1:]
    return s

def fs(st):
    return(st[0])

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
    bot.answer_callback_query(callback_query_id=call.id,)
    id = call.message.chat.id
    
    flag = fs(call.data)
    data = dt(call.data)
    list_of_service = data_from_sheet[0]
    for counter in range(2, len(list_of_service)):
        print(counter)
        if call.data  == '+'+ str(counter):
            add_servise_for_user(counter,id)
            edit_message(add_servise_for_user(counter,id))

        if call.data == '-' + str(counter):
            remove_servise_for_user(counter,id)    
            edit_message(remove_servise_for_user(counter,id))



print("Ready")
bot.infinity_polling()


