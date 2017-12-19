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