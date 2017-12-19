from order_item.order_item import OrderItem

class ItemBook(OrderItem):
    shipping_label = None
    
    def handle(self):
        self.shipping_label = self.generate_shipping_label()
        notification = "Item isento de impostos conforme disposto na Constituição Art. 150, VI, d."
        print("Shipping rules for book: {0}".format(notification))
        print("Book sent under shipping label: {0}".format(self.shipping_label))
