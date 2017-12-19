from order_item.order_item import OrderItem
from membership import Membership

class ItemMembership(OrderItem):
    
    def handle(self):
        new_membership = Membership(self.product.name)
        self.order.customer.add_membership(membership=new_membership)
        content = "Membership activated!"
        self.send_mail(content, self.order.customer.email)