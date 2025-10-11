from flask import Flask, jsonify, request
from flask_cors import CORS # For handling Cross-Origin Resource Sharing

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Sample product data
products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Mouse", "price": 25},
    {"id": 3, "name": "Keyboard", "price": 75},
]

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"message": "Product not found"}), 404

# Example of a simple order endpoint (requires more logic for a real e-commerce)
@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    # Process order data, save to database, etc.
    return jsonify({"message": "Order placed successfully", "order_details": data})

if __name__ == '__main__':
    app.run(debug=True, port=5000)