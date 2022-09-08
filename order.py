from services import ServicesManager
from tg_order_stages import OrderStage


class Order:
    def __init__(self, user_id, message_id):
        self.user_id = user_id
        self.message_id = message_id
        self.stage = OrderStage.BASIC_SERVICE
        self.basic_service = ServicesManager.basic_service

        # key: service type
        # value: amount of this service added to this order
        self.extra_services = {}
        for service_type in ServicesManager.extra_services:
            self.extra_services[service_type] = 0

    def add_service(self, service):
        self.extra_services[service] += 1

    def remove_service(self, service):
        if self.extra_services[service] > 0:
            self.extra_services[service] -= 1

    def get_total_price(self):
        total_price = self.basic_service.price
        for service in self.extra_services:
            total_price += service.price * self.extra_services[service]
        return total_price

    def get_total_time(self):
        total_time = self.basic_service.time
        for service in self.extra_services:
            total_time += service.time * self.extra_services[service]
        return total_time

    def get_amount_of_service(self, service):
        return self.extra_services[service]

    def get_next_stage(self):
        if self.stage == list(OrderStage)[-1]:
            raise Exception("Order is already at the last stage")

        return OrderStage(self.stage.value + 1)

    def get_previous_stage(self):
        if self.stage == list(OrderStage)[0]:
            raise Exception("Order is already at the first stage")

        return OrderStage(self.stage.value - 1)


class OrdersManager:
    orders = []

    @classmethod
    def add_order(cls, order):
        cls.orders.append(order)

    @classmethod
    def remove_order(cls, order):
        if order in cls.orders:
            cls.orders.remove(order)

    @classmethod
    def complete_order(cls, order):
        pass

    @classmethod
    def get_order(cls, user_id):
        return next(order for order in cls.orders if order.user_id == user_id)
