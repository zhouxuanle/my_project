// Table configuration to eliminate code duplication
export const TABLE_CONFIGS = {
  user: {
    label: 'User Table',
    columns: ['ID', 'Username', 'Real Name', 'Email', 'Phone', 'Sex', 'Age', 'Job', 'create_time'],
    fields: ['id', 'username', 'real_name', 'email', 'phone_number', 'sex', 'age', 'job', 'create_time']
  },
  address: {
    label: 'Address Table',
    columns: ['ID', 'User ID', 'Title', 'Address Line', 'Country', 'City', 'Postal Code', 'create_time'],
    fields: ['id', 'user_id', 'title', 'address_line', 'country', 'city', 'postal_code', 'create_time']
  },
  category: {
    label: 'Category Table',
    columns: ['ID', 'Name', 'Description', 'create_time'],
    fields: ['id', 'name', 'description', 'create_time']
  },
  subcategory: {
    label: 'Subcategory Table',
    columns: ['ID', 'Parent ID', 'Name', 'Description', 'create_time'],
    fields: ['id', 'parent_id', 'name', 'description', 'create_time']
  },
  product: {
    label: 'Product Table',
    columns: ['ID', 'Name', 'Description', 'Category ID', 'create_time'],
    fields: ['id', 'name', 'description', 'category_id', 'create_time']
  },
  products_sku: {
    label: 'Products SKU Table',
    columns: ['ID', 'Product ID', 'Price', 'Stock', 'create_time'],
    fields: ['id', 'product_id', 'price', 'stock', 'create_time']
  },
  wishlist: {
    label: 'Wishlist Table',
    columns: ['ID', 'User ID', 'Product SKU ID', 'create_time'],
    fields: ['id', 'user_id', 'products_sku_id', 'create_time']
  },
  payment: {
    label: 'Payment Table',
    columns: ['ID', 'Amount', 'Provider', 'Status', 'create_time'],
    fields: ['id', 'amount', 'provider', 'status', 'create_time']
  },
  order: {
    label: 'Order Table',
    columns: ['ID', 'User ID', 'Payment ID', 'create_time'],
    fields: ['id', 'user_id', 'payment_id', 'create_time']
  },
  order_item: {
    label: 'Order Item Table',
    columns: ['ID', 'Order ID', 'Product SKU ID', 'Quantity', 'create_time'],
    fields: ['id', 'order_id', 'products_sku_id', 'quantity', 'create_time']
  },
  cart: {
    label: 'Cart Table',
    columns: ['ID', 'Order ID', 'Product SKU ID', 'Quantity', 'create_time'],
    fields: ['id', 'order_id', 'products_sku_id', 'quantity', 'create_time']
  }
};

export const TABLE_LIST = Object.keys(TABLE_CONFIGS).map((key) => ({
  name: key,
  label: TABLE_CONFIGS[key].label,
}));