from services import ServicesManager
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from tg_order_stages import OrderStage

BUTTON_VALUE_SEPARATOR = ':'


class TgMessenger:
    def __init__(self, bot):
        self.bot = bot
        self.control_markup = self.draw_control_buttons(InlineKeyboardMarkup())

    # Start

    def send_start(self, user_id):
        message_text = "Приветствуем в нашем сервисе клинига \"Нежные пальчики\""
        self.bot.send_message(chat_id=user_id, text=message_text, reply_markup=self.draw_start_message_keyboard())

    @staticmethod
    def draw_start_message_keyboard():
        markup = InlineKeyboardMarkup()
        continue_btn = InlineKeyboardButton(text='Заказать клининг', callback_data='order_new')
        cancel_btn = InlineKeyboardButton(text='Меню', callback_data='menu')
        markup.row(continue_btn, cancel_btn)
        return markup

    # Basic service

    def send_basic_service(self, user_id):
        message_id = self.bot\
            .send_message(chat_id=user_id,
                          text=self.get_basic_service_message_text(),
                          reply_markup=self.control_markup)\
            .message_id
        return message_id

    def edit_to_basic_service(self, order):
        order.stage = OrderStage.BASIC_SERVICE
        self.bot.edit_message_text(chat_id=order.user_id,
                                   message_id=order.message_id,
                                   text=self.get_basic_service_message_text(),
                                   reply_markup=self.control_markup)

    @staticmethod
    def get_basic_service_message_text():
        return "Базовые услуги"

    # Extra services

    def edit_to_extra_services(self, order):
        order.stage = OrderStage.EXTRA_SERVICE
        message_text = "Дополнительные услуги"
        self.bot.edit_message_text(chat_id=order.user_id,
                                   message_id=order.message_id,
                                   text=message_text,
                                   reply_markup=self.extra_services_keyboard(order))

    def extra_services_keyboard(self, order):
        markup = InlineKeyboardMarkup()

        for service in ServicesManager.extra_services:
            markup = self\
                .service_buttons(service=service, amount_of_service=order.get_amount_of_service(service), markup=markup)

        return self.draw_control_buttons(markup)

    @staticmethod
    def service_buttons(service, amount_of_service, markup):
        title_msg = service.name if amount_of_service == 0 else f"{service.name} ({amount_of_service})"
        title_btn = InlineKeyboardButton(title_msg, callback_data='0')

        add_callback_data = '+' + BUTTON_VALUE_SEPARATOR + str(service.service_id)
        add_btn = InlineKeyboardButton(text='+', callback_data=add_callback_data)
        remove_callback_data = '-' + BUTTON_VALUE_SEPARATOR + str(service.service_id)
        remove_btn = InlineKeyboardButton(text='-', callback_data=remove_callback_data)

        markup.row(title_btn)
        markup.row(add_btn, remove_btn)
        return markup

    # Services confirmation

    def edit_to_services_confirmation(self, order):
        order.stage = OrderStage.SERVICES_CONFIRMATION
        message_text = f"Выбранные услуги:\n\n" \
                       f"Базовая уборка:  {order.basic_service.time}ч  -  {order.basic_service.price}руб;\n" \
                       f"{self.generate_selected_extra_services_info(order.extra_services)}\n" \
                       f"Итого:  {order.get_total_time()}ч  -  {order.get_total_price()}руб."

        self.bot.edit_message_text(chat_id=order.user_id,
                                   message_id=order.message_id,
                                   text=message_text,
                                   reply_markup=self.control_markup)

    @staticmethod
    def generate_selected_extra_services_info(services):
        info = ""
        for service in services:
            count_of_service = services[service]
            if count_of_service == 0:
                continue
            elif count_of_service == 1:
                info += f"{service.name}:  {service.time}ч  -  {service.price}руб;\n"
            else:
                info += f"{service.name}(x{count_of_service}):  " \
                        f"{service.time * count_of_service}ч  -  " \
                        f"{service.price * count_of_service}руб;\n"

        return info

    # Calendar

    def edit_to_calendar(self, order):
        order.stage = OrderStage.CALENDAR
        message_text = "Заглушка календарь"
        self.bot.edit_message_text(chat_id=order.user_id,
                                   message_id=order.message_id,
                                   text=message_text,
                                   reply_markup=self.control_markup)

    # Сlient contacts

    def edit_to_client_contacts(self, order):
        order.stage = OrderStage.CLIENT_CONTACTS
        message_text = "Заглушка контакты клиента"
        self.bot.edit_message_text(chat_id=order.user_id,
                                   message_id=order.message_id,
                                   text=message_text,
                                   reply_markup=self.control_markup)

    # Сomplete

    def edit_to_complete(self, order):
        message_text = "Заказ принят!\n" \
                       "В ближайшее время с вами свяжется администратор для подтверждения заказа"
        self.bot.edit_message_text(chat_id=order.user_id,
                                   message_id=order.message_id,
                                   text=message_text,
                                   reply_markup=self.control_markup)

    # Other

    @staticmethod
    def draw_control_buttons(markup):
        cancel_btn = InlineKeyboardButton(text='Отмена', callback_data='cancel')
        return_btn = InlineKeyboardButton(text='Назад', callback_data='return')
        continue_btn = InlineKeyboardButton(text='Продолжить', callback_data='continue')

        markup.row(cancel_btn, return_btn, continue_btn)
        return markup

    def delete_message(self, user_id, message_id):
        self.bot.delete_message(chat_id=user_id, message_id=message_id)

    def edit_to_stage(self, order, target_order_stage):
        print(f"target_stage - {target_order_stage.name}")
        if target_order_stage == OrderStage.BASIC_SERVICE:
            self.edit_to_basic_service(order)

        elif target_order_stage == OrderStage.EXTRA_SERVICE:
            self.edit_to_extra_services(order)

        elif target_order_stage == OrderStage.SERVICES_CONFIRMATION:
            self.edit_to_services_confirmation(order)

        elif target_order_stage == OrderStage.CALENDAR:
            self.edit_to_calendar(order)

        elif target_order_stage == OrderStage.CLIENT_CONTACTS:
            self.edit_to_client_contacts(order)
