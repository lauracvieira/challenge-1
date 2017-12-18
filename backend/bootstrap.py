#!/usr/bin/env python3
import time
from abc import ABC, abstractmethod
from uuid import uuid4 as uuid

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

class OrderItemHandler:
    order = None
    product = None
    def __init__(self, order):
        self.order = order

    def get_order_item(self, product):
        if product.type == "book":
            return ItemBook(order=self.order, product=product)
        elif product.type == "physical":
            return ItemPhysicalProduct(order=self.order, product=product)
        elif product.type == "digital":
            return ItemDigitalProduct(order=self.order, product=product)
        elif product.type == "membership":
            return ItemMembership(order=self.order, product=product)

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
        self.order.customer.add_membership(membership=new_membership)
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
        new_voucher = Voucher(discount=self.discount)
        self.order.customer.add_voucher(new_voucher)
        content = "Purchase of {0} completed successfully!".format(self.product.name)
        self.send_mail(content, self.order.customer.email)

class Voucher:
    value = None
    def __init__(self, discount):
        self.value = discount

class Product:
    # use type to distinguish each kind of product: physical, book, digital, membership, etc.
    produt_types = None
    name = None
    type = None

    def __init__(self, name, type):
        self.produt_types = ['book', 'digital', 'physical', 'membership']
        if type in self.produt_types:      
            self.name = name
            self.type = type
        else:
            raise ValueError("Product type must be one of the following: 'book', 'digital', 'physical' or 'membership'")

    def get_product_types(self):
        return self.produt_types

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

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.vouchers = []
        self.memberships = []

    def add_address(self, zipcode):
        self.address = Address(zipcode=zipcode)

    def add_voucher(self, voucher):
        if isinstance(voucher, Voucher):
            self.vouchers.append(voucher)
        else: 
            raise ValueError("Error adding Voucher")

    def add_membership(self, membership):
        if isinstance(membership, Membership):
            self.memberships.append(membership)
        else:
            raise ValueError("Error adding Membership")

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


foolano = Customer("Foolano", "foolano@gmail.com")
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
