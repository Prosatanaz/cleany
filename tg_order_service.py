from order import Order, OrdersManager


def create_order(user_id, message_id):
    new_order = Order(user_id=user_id, message_id=message_id)
    OrdersManager.add_order(new_order)


def delete_order(user_id):
    orders = OrdersManager.orders
    print(*orders)

    order = OrdersManager.get_order(user_id)
    OrdersManager.remove_order(order)



