import time
from order_item.order_item_handler import OrderItemHandler
from customer.address import Address
from payment.payment import Payment

class Order:
    customer = None
    items = None
    payment = None
    address = None
    closed_at = None

    def __init__(self, customer, attributes={}):
        self.customer = customer
        self.items = []
        self.order_item_handler = OrderItemHandler(order=self)
        self.address = attributes.get('address', Address(zipcode='45678-979'))

    def add_product(self, product):
        item = self.order_item_handler.get_order_item(product=product)
        self.items.append(item)

    def total_amount(self):
        total = 0
        for item in items:
            total += item.total

        return total

    def close(self, closed_at=time.time()):
        self.closed_at = closed_at

    def pay(self, attributes):
        self.payment = Payment(attributes=attributes)
        self.payment.pay()

    def handle_shipping_rules(self):
        try:
            if self.payment.is_paid():
                for item in self.items:
                    item.handle()
        except:
            raise ValueError("Order must be paid before handling shipping rules")
