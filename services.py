class ExtraService:
    def __init__(self, service_id, name, time, price, message):
        self.service_id = service_id
        self.name = name
        self.time = time
        self.price = price
        self.message = message


class ServicesManager:
    services_types = []

    @classmethod
    def set_services_types(cls, tabel):
        # remove table header
        del tabel[0]

        service_id = 0
        for row in tabel:
            new_service = ExtraService(service_id=service_id, name=row[0], time=row[1], price=row[2], message=row[3])
            cls.services_types.append(new_service)
            service_id += 1

    @classmethod
    def get_service(cls, service_id):
        return next(service for service in cls.services_types if str(service.service_id) == service_id)
