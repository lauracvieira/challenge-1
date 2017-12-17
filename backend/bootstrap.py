import time
from abc import ABC, abstractmethod
import uuid

class Payment():
    authorization_number = None
    amount = None
    invoice = None
    order = None
    payment_method = None
    paid_at = None

    def __init__(self, attributes={}):
        self.authorization_number = attributes.get('attributes', None)
        self.amount = attributes.get('amount', None)
        self.invoice = attributes.get('invoice', None)
        self.order = attributes.get('order', None)
        self.payment_method = attributes.get('payment_method', None)

    def pay(self, paid_at=time.time()):
        self.amount = self.order.total_amount
        self.authorization_number = int(time.time())
        attributes = dict(
            billing_address=self.order.address,
            shipping_address=self.order.address,
            order=self.order
        )
        self.invoice = Invoice(attributes=attributes)
        self.paid_at = paid_at
        self.order.close(self.paid_at)

    def is_paid(self):
        return self.paid_at != None

class Invoice:
    billing_address = None
    shipping_address = None
    order = None

    def __init__(self, attributes={}):
        self.billing_address = attributes.get('billing_address', None)
        self.shipping_address = attributes.get('shipping_address', None)
        self.order = attributes.get('order', None)


class Order:
    customer = None
    items = None
    payment = None
    address = None
    closed_at = None

    def __init__(self, customer, attributes={}):
        self.customer = customer
        self.items = []
        self.address = attributes.get('address', Address(zipcode='45678-979'))

    def add_product(self, product):
        if product.type == "book":
            self.items.append(ItemBook(self, product))
        elif product.type == "physical":
            self.items.append(ItemPhysicalProduct(self, product))
        elif product.type == "digital":
            self.items.append(ItemDigitalProduct(self, product))
        elif product.type == "membership":
            self.items.append(ItemMembership(self, product))

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
        if self.payment.is_paid():
            for item in self.items:
                item.handle()

class OrderItem(ABC):
    order = None
    product = None

    def __init__(self, order, product):
        self.order = order
        self.product = product

    def total(self):
        return 10

    def generate_shipping_label(self):
        return (uuid.uuid4())

    def send_mail(self, content, email):
        print("Sending mail to {0}".format(email))
        print(content)

    @abstractmethod
    def handle(self):
        pass

class ItemPhysicalProduct(OrderItem):
    shipping_label = None
    def handle(self):
        print(" ---- FISICO ---- ")
        self.shipping_label = self.generate_shipping_label()        
        print("Item sent under shipping label: {0}".format(self.shipping_label))

class ItemMembership(OrderItem):
    def handle(self):
        print(" ---- ASSINATURA ---- ")
        new_membership = Membership(self.product.name)
        self.order.customer.add_membership(new_membership)
        content = "Membership activated!"
        self.send_mail(content, self.order.customer.email)

class ItemBook(OrderItem):
    shipping_label = None
    def handle(self):
        print(" ---- LIVRO ---- ")
        self.shipping_label = self.generate_shipping_label()
        notification = "Item isento de impostos conforme disposto na Constituição Art. 150, VI, d."
        print("Shipping rules for book: {0}".format(notification))
        print("Book sent under shipping label: {0}".format(self.shipping_label))

class ItemDigitalProduct(OrderItem):
    discount = 10
    def handle(self):
        print(" ---- DIGITAL ---- ")
        new_voucher = Voucher(self.discount)
        self.order.customer.add_voucher(new_voucher)
        content = "Purchase of {0} completed successfully!".format(self.product.name)
        self.send_mail(content, self.order.customer.email)

class Voucher:
    value = None
    def __init__(self, discount):
        self.value = discount

class Product:
    # use type to distinguish each kind of product: physical, book, digital, membership, etc.
    name = None
    type = None
    payment = None

    def __init__(self, name, type):
        self.name = name
        self.type = type

class Address:
    zipcode = None

    def __init__(self, zipcode):
        self.zipcode = zipcode

class CreditCard:

    @staticmethod
    def fetch_by_hashed(code):
        return CreditCard()

class Customer:
    name = None
    last_name = None
    email = None
    vouchers = None
    address = None
    memberships = None

    def __init__(self, name, email, zipcode):
        self.name = name
        self.email = email
        self.vouchers = []
        self.memberships = []
        self.address = Address(zipcode)

    def add_voucher(self, voucher):
        self.vouchers.append(voucher)

    def add_membership(self, membership):
        self.memberships.append(membership)

class Membership:
    name = None
    activated_at = None
    deactivated_at = None

    def __init__(self, name, activated_at=time.time()):
        self.name = name
        self.activated_at = activated_at

    def deactivate(self, deactivated_at=time.time()):
        self.deactivated_at = deactivated_at

    def is_active(self):
        return (activated_at != None and deactivated_at == None)


foolano = Customer("Foolano", "foolano@gmail.com", "00000-000")
physical = Product(name='Fridge', type='physical')
membership = Product(name='Amazon Prime', type='membership')
book = Product(name='Awesome book', type='book')
digital = Product(name='Ebook Harry Potter', type='digital')

my_order = Order(foolano)
my_order.add_product(physical)
my_order.add_product(membership)
my_order.add_product(book)
my_order.add_product(digital)


attributes = dict(
    order=my_order,
    payment_method=CreditCard.fetch_by_hashed('43567890-987654367')
)
my_order.pay(attributes=attributes)
my_order.handle_shipping_rules()

for membership in foolano.memberships:
    print(membership.name)

for voucher in foolano.vouchers:
    print(voucher.value)
# now, how to deal with shipping rules then?
