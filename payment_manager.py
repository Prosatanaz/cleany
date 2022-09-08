from yoomoney import Client
from yoomoney import Quickpay


class paymentManager:
    def __init__(self):
        self.token = '4100117957739405.D6D2466AABB0466D626D1E4B21F5B6572439DFA34EEAEDB9FBC5CAC6D17BAEDE4CD2A6BFEC22238C0D357DD34C4917A8FEACB77BBBB088C688E71EE0538BEE2A58E41E0CB89936EC18B1C5F68A8EF3F0287C8A18DA366CAF56F0CE2EBA717C6698B74EE7B93B272140726272F5D1214E133E2AE9FAE46D81180B6556A649A00C'
        self.client = Client(self.token)
        self.user = self.client.account_info()

    def get_pay_url(self, price, client_id, order_data):
        label = client_id + order_data
        quickpay = Quickpay(receiver="4100117957739405", quickpay_form="shop", targets="Sponsor this project",
                            paymentType="SB", sum=price, label=label, )
        pay_url = quickpay.base_url
        return pay_url

    def check_status_operation(self, client_id, order_data):
        history = self.client.operation_history(label=client_id + order_data)
        #находим операции по фильтру label
        for operation in history.operations:
            operation_id = operation.operation_id
            operation_status =  operation.status
        return operation_status, operation_id
