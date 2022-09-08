from enum import Enum


class OrderStage(Enum):
    BASIC_SERVICE = 0
    EXTRA_SERVICE = 1
    SERVICES_CONFIRMATION = 2
    CALENDAR = 3
    CLIENT_CONTACTS = 4

