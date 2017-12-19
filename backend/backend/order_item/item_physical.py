from order_item.order_item import OrderItem

class ItemPhysical(OrderItem):
    shipping_label = None
    
    def handle(self):
        self.shipping_label = self.generate_shipping_label()        
        print("Item sent under shipping label: {0}".format(self.shipping_label))
