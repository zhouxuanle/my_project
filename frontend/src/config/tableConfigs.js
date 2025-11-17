// Table configuration to eliminate code duplication
export const TABLE_CONFIGS = {
  user: {
    label: 'User Table',
    columns: ['ID', 'Username', 'Real Name', 'Email', 'Phone', 'Sex', 'Age', 'Job', 'created_at'],
    fields: ['id', 'user_name', 'real_name', 'email', 'phone_number', 'sex', 'age', 'job', 'created_at']
  },
  address: {
    label: 'Address Table',
    columns: ['ID', 'User ID', 'Title', 'Address Line', 'Country', 'City', 'Postal Code', 'created_at'],
    fields: ['id', 'user_id', 'title', 'address_line', 'country', 'city', 'postal_code', 'created_at']
  },
  category: {
    label: 'Category Table',
    columns: ['ID', 'Name', 'Description', 'created_at'],
    fields: ['id', 'name', 'description', 'created_at']
  },
  subcategory: {
    label: 'Subcategory Table',
    columns: ['ID', 'Parent ID', 'Name', 'Description', 'created_at'],
    fields: ['id', 'parent_id', 'name', 'description', 'created_at']
  },
  product: {
    label: 'Product Table',
    columns: ['ID', 'Name', 'Description', 'Category ID', 'created_at'],
    fields: ['id', 'name', 'description', 'category_id', 'created_at']
  },
  products_sku: {
    label: 'Products SKU Table',
    columns: ['ID', 'Product ID', 'Price', 'Stock', 'created_at'],
    fields: ['id', 'product_id', 'price', 'stock', 'created_at']
  },
  wishlist: {
    label: 'Wishlist Table',
    columns: ['ID', 'User ID', 'Product SKU ID', 'created_at'],
    fields: ['id', 'user_id', 'products_sku_id', 'created_at']
  },
  payment: {
    label: 'Payment Table',
    columns: ['ID', 'Amount', 'Provider', 'Status', 'created_at'],
    fields: ['id', 'amount', 'provider', 'status', 'created_at']
  },
  order: {
    label: 'Order Table',
    columns: ['ID', 'User ID', 'Payment ID', 'created_at'],
    fields: ['id', 'user_id', 'payment_id', 'created_at']
  },
  order_item: {
    label: 'Order Item Table',
    columns: ['ID', 'Order ID', 'Product SKU ID', 'Quantity', 'created_at'],
    fields: ['id', 'order_id', 'products_sku_id', 'quantity', 'created_at']
  },
  cart: {
    label: 'Cart Table',
    columns: ['ID', 'Order ID', 'Product SKU ID', 'Quantity', 'created_at'],
    fields: ['id', 'order_id', 'products_sku_id', 'quantity', 'created_at']
  }
};