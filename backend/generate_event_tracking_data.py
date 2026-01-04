class DataGenerator:
    def __init__(self):
        pass

    # Generate user_info Table Data
    def generate_user_data(self):
        from data_generators.user_table.user_data import generate_user_data
        return generate_user_data()

    # Generate Address Table Data
    def generate_fake_address(self, user):
        from data_generators.address_table.address_data import generate_fake_address
        return generate_fake_address(user)


    # Generate Categories Table Data
    def generate_categories_data(self):
        from data_generators.categories_table.categories_data import generate_categories_data
        return generate_categories_data()


    # Generate Subcategories Table Data
    def generate_subcategories_data(self, category):
        from data_generators.subcategories_table.subcategories_data import generate_subcategories_data
        return generate_subcategories_data(category)


    # Generate Products Table Data
    def generate_products_data(self, subcategory):
        from data_generators.products_table.products_data import generate_products_data
        return generate_products_data(subcategory)


    # Generate product_sku Table Data
    def generate_sku_data(self, category, subcategory, product):
        from data_generators.product_sku_table.sku_data import generate_sku_data
        return generate_sku_data(category, subcategory, product)

    # Generate Wishlist Table Data
    def generate_wishlist_data(self, products_sku, user):
        from data_generators.wishlist_table.wishlist_data import generate_wishlist_data
        return generate_wishlist_data(products_sku, user)

    # Generate Order_details Table Data
    def generate_order_details_data(self, user, payment):
        from data_generators.order_details_table.order_details_data import generate_order_details_data
        return generate_order_details_data(user, payment)


    # Generate Order_item Table Data
    def generate_order_item_data(self, products_sku, order):
        from data_generators.order_item_table.order_item_data import generate_order_item_data
        return generate_order_item_data(products_sku, order)


    # Generate Payment_details Table Data
    def generate_payment_details_data(self):
        from data_generators.payment_details_table.payment_details_data import generate_payment_details_data
        return generate_payment_details_data()




