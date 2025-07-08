from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient('mongodb+srv://benaiahraini:fYKbT8O8ScARZZUP@cluster0.qulhqkk.mongodb.net/')
db = client['pika_light_grocery']

# Collections
items_collection = db['items']
orders_collection = db['orders']
carts_collection = db['carts']

#data initialization
def init_sample_data():
    """Initialize the database with sample grocery items"""
    if items_collection.count_documents({}) == 0:
        sample_items = [
            # Fruits
            {"name": "Apples", "category": "Fruits", "price": 2.99, "stock": 50, "description": "Fresh red apples"},
            {"name": "Bananas", "category": "Fruits", "price": 1.49, "stock": 30, "description": "Ripe yellow bananas"},
            {"name": "Oranges", "category": "Fruits", "price": 3.49, "stock": 25, "description": "Juicy oranges"},
            {"name": "Strawberries", "category": "Fruits", "price": 4.99, "stock": 15, "description": "Sweet strawberries"},
            
            # Dairy
            {"name": "Milk", "category": "Dairy", "price": 3.29, "stock": 40, "description": "Whole milk 1L"},
            {"name": "Cheese", "category": "Dairy", "price": 5.99, "stock": 20, "description": "Cheddar cheese block"},
            {"name": "Yogurt", "category": "Dairy", "price": 1.99, "stock": 35, "description": "Greek yogurt 500g"},
            {"name": "Butter", "category": "Dairy", "price": 4.49, "stock": 25, "description": "Unsalted butter"},
            
            # Vegetables
            {"name": "Carrots", "category": "Vegetables", "price": 1.99, "stock": 45, "description": "Fresh carrots 1kg"},
            {"name": "Broccoli", "category": "Vegetables", "price": 2.79, "stock": 30, "description": "Fresh broccoli head"},
            {"name": "Tomatoes", "category": "Vegetables", "price": 3.99, "stock": 20, "description": "Ripe tomatoes 1kg"},
            {"name": "Lettuce", "category": "Vegetables", "price": 2.49, "stock": 25, "description": "Fresh lettuce head"},
            
            # Meat
            {"name": "Chicken Breast", "category": "Meat", "price": 8.99, "stock": 15, "description": "Fresh chicken breast 1kg"},
            {"name": "Ground Beef", "category": "Meat", "price": 12.99, "stock": 10, "description": "Ground beef 1kg"},
            {"name": "Salmon", "category": "Meat", "price": 16.99, "stock": 8, "description": "Fresh salmon fillet"},
            
            # Pantry
            {"name": "Rice", "category": "Pantry", "price": 4.99, "stock": 50, "description": "Basmati rice 2kg"},
            {"name": "Pasta", "category": "Pantry", "price": 2.99, "stock": 40, "description": "Spaghetti pasta 500g"},
            {"name": "Olive Oil", "category": "Pantry", "price": 7.99, "stock": 30, "description": "Extra virgin olive oil 500ml"},
        ]
        items_collection.insert_many(sample_items)
        print("Sample data initialized!")

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc:
        doc['_id'] = str(doc['_id'])
    return doc

def serialize_docs(docs):
    """Convert list of MongoDB documents to JSON serializable format"""
    return [serialize_doc(doc) for doc in docs]

# Routes

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to PIKA-LIGHT Grocery Delivery API",
        "version": "1.0.0",
        "endpoints": {
            "GET /items": "Get all items or search by category/name",
            "GET /items/<id>": "Get specific item",
            "POST /cart": "Add item to cart",
            "GET /cart/<user_id>": "Get user's cart",
            "DELETE /cart/<user_id>/<item_id>": "Remove item from cart",
            "POST /orders": "Place an order",
            "GET /orders/<user_id>": "Get user's order history"
        }
    })

# Items endpoints
@app.route('/items', methods=['GET'])
def get_items():
    """Get all items or filter by category/search"""
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = {}
    if category:
        query['category'] = {'$regex': category, '$options': 'i'}
    if search:
        query['$or'] = [
            {'name': {'$regex': search, '$options': 'i'}},
            {'description': {'$regex': search, '$options': 'i'}}
        ]
    
    items = list(items_collection.find(query))
    return jsonify(serialize_docs(items))

@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item by ID"""
    try:
        item = items_collection.find_one({'_id': ObjectId(item_id)})
        if item:
            return jsonify(serialize_doc(item))
        return jsonify({'error': 'Item not found'}), 404
    except:
        return jsonify({'error': 'Invalid item ID'}), 400

@app.route('/categories', methods=['GET'])
def get_categories():
    """Get all available categories"""
    categories = items_collection.distinct('category')
    return jsonify(categories)

# Cart endpoints
@app.route('/cart', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    
    required_fields = ['user_id', 'item_id', 'quantity']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Check if item exists
        item = items_collection.find_one({'_id': ObjectId(data['item_id'])})
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Check stock
        if item['stock'] < data['quantity']:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        # Check if item already in cart
        existing_cart_item = carts_collection.find_one({
            'user_id': data['user_id'],
            'item_id': data['item_id']
        })
        
        if existing_cart_item:
            # Update quantity
            new_quantity = existing_cart_item['quantity'] + data['quantity']
            if item['stock'] < new_quantity:
                return jsonify({'error': 'Insufficient stock'}), 400
            
            carts_collection.update_one(
                {'_id': existing_cart_item['_id']},
                {'$set': {'quantity': new_quantity}}
            )
        else:
            # Add new cart item
            cart_item = {
                'user_id': data['user_id'],
                'item_id': data['item_id'],
                'quantity': data['quantity'],
                'added_at': datetime.now()
            }
            carts_collection.insert_one(cart_item)
        
        return jsonify({'message': 'Item added to cart successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    """Get user's cart with item details"""
    try:
        # Get cart items
        cart_items = list(carts_collection.find({'user_id': user_id}))
        
        # Get item details for each cart item
        cart_with_details = []
        total_price = 0
        
        for cart_item in cart_items:
            item = items_collection.find_one({'_id': ObjectId(cart_item['item_id'])})
            if item:
                cart_detail = {
                    'cart_id': str(cart_item['_id']),
                    'item_id': cart_item['item_id'],
                    'name': item['name'],
                    'price': item['price'],
                    'quantity': cart_item['quantity'],
                    'subtotal': item['price'] * cart_item['quantity']
                }
                cart_with_details.append(cart_detail)
                total_price += cart_detail['subtotal']
        
        return jsonify({
            'user_id': user_id,
            'items': cart_with_details,
            'total_price': round(total_price, 2),
            'item_count': len(cart_with_details)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cart/<user_id>/<item_id>', methods=['DELETE'])
def remove_from_cart(user_id, item_id):
    """Remove item from cart"""
    try:
        result = carts_collection.delete_one({
            'user_id': user_id,
            'item_id': item_id
        })
        
        if result.deleted_count > 0:
            return jsonify({'message': 'Item removed from cart'})
        else:
            return jsonify({'error': 'Item not found in cart'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cart/<user_id>', methods=['DELETE'])
def clear_cart(user_id):
    """Clear user's cart"""
    try:
        carts_collection.delete_many({'user_id': user_id})
        return jsonify({'message': 'Cart cleared successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Orders endpoints
@app.route('/orders', methods=['POST'])
def place_order():
    """Place an order from cart"""
    data = request.get_json()
    
    if 'user_id' not in data:
        return jsonify({'error': 'User ID required'}), 400
    
    user_id = data['user_id']
    
    try:
        # Get cart items
        cart_items = list(carts_collection.find({'user_id': user_id}))
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Prepare order items and calculate total
        order_items = []
        total_price = 0
        
        for cart_item in cart_items:
            item = items_collection.find_one({'_id': ObjectId(cart_item['item_id'])})
            if item:
                # Check stock again
                if item['stock'] < cart_item['quantity']:
                    return jsonify({'error': f'Insufficient stock for {item["name"]}'}), 400
                
                order_item = {
                    'item_id': cart_item['item_id'],
                    'name': item['name'],
                    'price': item['price'],
                    'quantity': cart_item['quantity'],
                    'subtotal': item['price'] * cart_item['quantity']
                }
                order_items.append(order_item)
                total_price += order_item['subtotal']
                
                # Update stock
                items_collection.update_one(
                    {'_id': ObjectId(cart_item['item_id'])},
                    {'$inc': {'stock': -cart_item['quantity']}}
                )
        
        # Create order
        order = {
            'user_id': user_id,
            'items': order_items,
            'total_price': round(total_price, 2),
            'status': 'pending',
            'order_date': datetime.now(),
            'delivery_address': data.get('delivery_address', ''),
            'contact_phone': data.get('contact_phone', '')
        }
        
        result = orders_collection.insert_one(order)
        
        # Clear cart
        carts_collection.delete_many({'user_id': user_id})
        
        return jsonify({
            'message': 'Order placed successfully',
            'order_id': str(result.inserted_id),
            'total_price': order['total_price']
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/orders/<user_id>', methods=['GET'])
def get_orders(user_id):
    """Get user's order history"""
    try:
        orders = list(orders_collection.find({'user_id': user_id}).sort('order_date', -1))
        return jsonify(serialize_docs(orders))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/orders/<user_id>/<order_id>', methods=['GET'])
def get_order(user_id, order_id):
    """Get specific order details"""
    try:
        order = orders_collection.find_one({
            '_id': ObjectId(order_id),
            'user_id': user_id
        })
        
        if order:
            return jsonify(serialize_doc(order))
        return jsonify({'error': 'Order not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin endpoints (bonus)
@app.route('/admin/items', methods=['POST'])
def add_item():
    """Add new item (admin only)"""
    data = request.get_json()
    
    required_fields = ['name', 'category', 'price', 'stock']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        item = {
            'name': data['name'],
            'category': data['category'],
            'price': float(data['price']),
            'stock': int(data['stock']),
            'description': data.get('description', ''),
            'created_at': datetime.now()
        }
        
        result = items_collection.insert_one(item)
        return jsonify({
            'message': 'Item added successfully',
            'item_id': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    """Update item (admin only)"""
    data = request.get_json()
    
    try:
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'category' in data:
            update_data['category'] = data['category']
        if 'price' in data:
            update_data['price'] = float(data['price'])
        if 'stock' in data:
            update_data['stock'] = int(data['stock'])
        if 'description' in data:
            update_data['description'] = data['description']
        
        result = items_collection.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': update_data}
        )
        
        if result.matched_count > 0:
            return jsonify({'message': 'Item updated successfully'})
        else:
            return jsonify({'error': 'Item not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_sample_data()
    print(" PIKA-LIGHT Grocery Delivery API is starting...")
    print(" data initialized")
    print(" API running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
