import gspread
from order import Order, OrdersManager
from services import ServicesManager
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BUTTON_VALUE_SEPARATOR = ':'


def draw_extra_services_keyboard(order):
    markup = InlineKeyboardMarkup()

    for service in ServicesManager.services_types:
        pass
        markup = draw_service_buttons(service=service, amount_of_service=order.get_amount_of_service(), markup=markup)

    return draw_control_buttons(markup)


def draw_service_offer():
    return draw_control_buttons(InlineKeyboardMarkup())


def draw_service_buttons(service, amount_of_service, markup):
    title_msg = service.name if amount_of_service == 0 else f"{service.name} ({amount_of_service})"
    title_btn = InlineKeyboardButton(title_msg, callback_data='0')
    add_btn = InlineKeyboardButton(text='+', callback_data='+' + BUTTON_VALUE_SEPARATOR + str(service.service_id))
    remove_btn = InlineKeyboardButton(text='-', callback_data='-' + BUTTON_VALUE_SEPARATOR + str(service.service_id))

    markup.row(title_btn)
    markup.row(add_btn, remove_btn)
    return markup


def draw_control_buttons(markup):
    continue_btn = InlineKeyboardButton(text='Продолжить', callback_data='continue')
    cancel_btn = InlineKeyboardButton(text='Отмена', callback_data='cancel')
    markup.row(continue_btn, cancel_btn)
    return markup


def get_services_data_from_sheet():
    gc = gspread.service_account(filename="clinny-361618-f313b3437739.json")
    calc_sheet_url = gc.open_by_url('https://docs.google.com/spreadsheets/d/'
                                    '115gY9pcQghGnjV5FLfnDZELuTu6invP72rK40sb3em8/edit#gid=480424214')
    return calc_sheet_url.get_worksheet(4).get_all_values()


def take_order(bot, user_id):
    message_text = "Приветствуем в нашем сервисе клинига \"Нежные пальчики\""
    message_id = bot.send_message(chat_id=user_id, text=message_text, reply_markup=draw_service_offer()).message_id

    ServicesManager.set_services_types(tabel=get_services_data_from_sheet())
    new_order = Order(user_id=user_id, message_id=message_id)
    OrdersManager.add_order(new_order)


def edit_message(bot, order, text, markup):
    bot.edit_message_text(text=text, chat_id=order.user_id, message_id=order.message_id, reply_markup=markup)


def edit_to_extra_services(bot, user_id):
    order = OrdersManager.get_order(user_id)
    message_text = "Можете выбрать дополнительные услуги услуги"
    markup = draw_extra_services_keyboard(order)
    edit_message(bot, order, message_text, markup)


def cancel_order(bot, user_id):
    order = OrdersManager.get_order(user_id)
    bot.delete_message(chat_id=order.user_id, message_id=order.message_id)
    OrdersManager.remove_order(order)


def add_remove_buttons_handler(user_id, user_answer):
    # user_answer consists of 2 parts - is needed to add or remove service and service id
    splitted_user_answer = user_answer.split(BUTTON_VALUE_SEPARATOR)
    is_add = splitted_user_answer[0] == "+"
    service_id = splitted_user_answer[1]

    order = OrdersManager.get_order(user_id)
    service = ServicesManager.get_service(service_id)

    if is_add:
        order.add_service(service)
    else:
        order.remove_service(service)
