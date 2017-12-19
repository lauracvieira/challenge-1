from order_item.item_book import ItemBook
from order_item.item_physical import ItemPhysical
from order_item.item_digital import ItemDigital
from order_item.item_membership import ItemMembership
class OrderItemHandler:
    order = None
    product = None
    def __init__(self, order):
        self.order = order

    def get_order_item(self, product):
        if product.type == "book":
            return ItemBook(order=self.order, product=product)
        elif product.type == "physical":
            return ItemPhysical(order=self.order, product=product)
        elif product.type == "digital":
            return ItemDigital(order=self.order, product=product)
        elif product.type == "membership":
            return ItemMembership(order=self.order, product=product)