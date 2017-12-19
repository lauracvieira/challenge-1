from membership import Membership
from voucher import Voucher

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