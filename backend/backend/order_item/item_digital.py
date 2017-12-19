from order_item.order_item import OrderItem
from voucher import Voucher

class ItemDigital(OrderItem):
    discount = 10
    
    def handle(self):
        new_voucher = Voucher(discount=self.discount)
        self.order.customer.add_voucher(new_voucher)
        content = "Purchase of {0} completed successfully!".format(self.product.name)
        self.send_mail(content, self.order.customer.email)