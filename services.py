class BasicService:
    def __init__(self, price, time):
        self.price = price
        self.time = time


class ExtraService:
    def __init__(self, service_id, name, price, time, message):
        self.service_id = service_id
        self.name = name
        self.price = price
        self.time = time
        self.message = message


class ServicesManager:
    basic_service = None
    extra_services = []

    @classmethod
    def set_basic_service(cls, tabel):
        # get first value row ignoring table header
        row = tabel[1]
        cls.basic_service = BasicService(price=float(row[0]),
                                         time=float(row[1]))

    @classmethod
    def set_extra_services(cls, tabel):
        # remove table header
        del tabel[0]

        services = []
        service_id = 0
        for row in tabel:
            new_service = ExtraService(service_id=service_id,
                                       name=row[0],
                                       price=float(row[1]),
                                       time=float(row[2]),
                                       message=row[3])
            services.append(new_service)
            service_id += 1
        cls.extra_services = services

    @classmethod
    def get_service(cls, service_id):
        return next(service for service in cls.extra_services if str(service.service_id) == service_id)
