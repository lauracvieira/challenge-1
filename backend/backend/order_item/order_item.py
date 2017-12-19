from uuid import uuid4 as uuid
from abc import ABC, abstractmethod

class OrderItem(ABC):
    order = None
    product = None

    def __init__(self, order, product):
        self.order = order
        self.product = product

    def total(self):
        return 10

    def generate_shipping_label(self):
        return (uuid())

    def send_mail(self, content, email):
        print("Sending mail to {0}".format(email))
        print(content)

    @abstractmethod
    def handle(self):
        pass