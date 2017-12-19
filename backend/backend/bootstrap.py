#!/usr/bin/env python3
from payment.payment import Payment
from order import Order
from customer.customer import Customer
from product import Product
from customer.credit_card import CreditCard

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