# 🛒 PIKA-LIGHT API Documentation

## Overview

The PIKA-LIGHT API is a RESTful web service that provides endpoints for managing products, shopping carts, and orders in a grocery delivery application. The API is built with Flask and uses MongoDB for data storage.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API uses a simple user ID system for demonstration purposes. In production, implement JWT authentication.

**Demo User ID**: `user123`

## Content Type

All requests and responses use JSON format:
```
Content-Type: application/json
```

## Response Format

### Success Response
```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "code": 400
}
```

## Endpoints

### Products

#### Get All Products
Retrieve all products from the catalog.

```http
GET /items
```

**Query Parameters:**
- `category` (optional): Filter by category (Fruits, Dairy, Vegetables, Meat, Pantry)
- `search` (optional): Search products by name

**Example Requests:**
```bash
# Get all products
curl http://localhost:5000/items

# Filter by category
curl http://localhost:5000/items?category=Fruits

# Search products
curl http://localhost:5000/items?search=apple
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "_id": "65a1b2c3d4e5f6789012345",
      "name": "Fresh Apples",
      "category": "Fruits",
      "price": 2.99,
      "stock": 50,
      "description": "Crisp and juicy red apples"
    }
  ]
}
```

#### Get Product by ID
Retrieve a specific product by its ID.

```http
GET /items/<id>
```

**Parameters:**
- `id` (required): MongoDB ObjectId of the product

**Example Request:**
```bash
curl http://localhost:5000/items/65a1b2c3d4e5f6789012345
```

**Response:**
```json
{
  "success": true,
  "data": {
    "_id": "65a1b2c3d4e5f6789012345",
    "name": "Fresh Apples",
    "category": "Fruits",
    "price": 2.99,
    "stock": 50,
    "description": "Crisp and juicy red apples"
  }
}
```

#### Get Categories
Retrieve all available product categories.

```http
GET /categories
```

**Example Request:**
```bash
curl http://localhost:5000/categories
```

**Response:**
```json
{
  "success": true,
  "data": [
    "Fruits",
    "Dairy",
    "Vegetables",
    "Meat",
    "Pantry"
  ]
}
```

### Shopping Cart

#### Add Item to Cart
Add a product to the user's shopping cart.

```http
POST /cart
```

**Request Body:**
```json
{
  "user_id": "user123",
  "item_id": "65a1b2c3d4e5f6789012345",
  "quantity": 2
}
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/cart \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "item_id": "65a1b2c3d4e5f6789012345",
    "quantity": 2
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Item added to cart",
  "data": {
    "_id": "65a1b2c3d4e5f6789012346",
    "user_id": "user123",
    "item_id": "65a1b2c3d4e5f6789012345",
    "quantity": 2,
    "added_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Get User Cart
Retrieve all items in a user's cart.

```http
GET /cart/<user_id>
```

**Parameters:**
- `user_id` (required): User identifier

**Example Request:**
```bash
curl http://localhost:5000/cart/user123
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "_id": "65a1b2c3d4e5f6789012346",
      "user_id": "user123",
      "item_id": "65a1b2c3d4e5f6789012345",
      "quantity": 2,
      "added_at": "2024-01-15T10:30:00Z",
      "item_details": {
        "name": "Fresh Apples",
        "price": 2.99,
        "category": "Fruits"
      }
    }
  ]
}
```

#### Remove Item from Cart
Remove a specific item from the user's cart.

```http
DELETE /cart/<user_id>/<item_id>
```

**Parameters:**
- `user_id` (required): User identifier
- `item_id` (required): Product ID to remove

**Example Request:**
```bash
curl -X DELETE http://localhost:5000/cart/user123/65a1b2c3d4e5f6789012345
```

**Response:**
```json
{
  "success": true,
  "message": "Item removed from cart"
}
```

#### Clear Cart
Remove all items from the user's cart.

```http
DELETE /cart/<user_id>
```

**Parameters:**
- `user_id` (required): User identifier

**Example Request:**
```bash
curl -X DELETE http://localhost:5000/cart/user123
```

**Response:**
```json
{
  "success": true,
  "message": "Cart cleared"
}
```

### Orders

#### Place Order
Create a new order from the user's cart.

```http
POST /orders
```

**Request Body:**
```json
{
  "user_id": "user123",
  "delivery_address": "123 Main St, City, State 12345",
  "contact_phone": "555-1234"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "delivery_address": "123 Main St, City, State 12345",
    "contact_phone": "555-1234"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Order placed successfully",
  "data": {
    "_id": "65a1b2c3d4e5f6789012347",
    "user_id": "user123",
    "items": [
      {
        "item_id": "65a1b2c3d4e5f6789012345",
        "name": "Fresh Apples",
        "price": 2.99,
        "quantity": 2,
        "subtotal": 5.98
      }
    ],
    "total_price": 5.98,
    "status": "pending",
    "order_date": "2024-01-15T10:30:00Z",
    "delivery_address": "123 Main St, City, State 12345",
    "contact_phone": "555-1234"
  }
}
```

#### Get Order History
Retrieve all orders for a user.

```http
GET /orders/<user_id>
```

**Parameters:**
- `user_id` (required): User identifier

**Example Request:**
```bash
curl http://localhost:5000/orders/user123
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "_id": "65a1b2c3d4e5f6789012347",
      "user_id": "user123",
      "items": [
        {
          "item_id": "65a1b2c3d4e5f6789012345",
          "name": "Fresh Apples",
          "price": 2.99,
          "quantity": 2,
          "subtotal": 5.98
        }
      ],
      "total_price": 5.98,
      "status": "pending",
      "order_date": "2024-01-15T10:30:00Z",
      "delivery_address": "123 Main St, City, State 12345",
      "contact_phone": "555-1234"
    }
  ]
}
```

#### Get Specific Order
Retrieve a specific order by its ID.

```http
GET /orders/<user_id>/<order_id>
```

**Parameters:**
- `user_id` (required): User identifier
- `order_id` (required): Order ID

**Example Request:**
```bash
curl http://localhost:5000/orders/user123/65a1b2c3d4e5f6789012347
```

**Response:**
```json
{
  "success": true,
  "data": {
    "_id": "65a1b2c3d4e5f6789012347",
    "user_id": "user123",
    "items": [
      {
        "item_id": "65a1b2c3d4e5f6789012345",
        "name": "Fresh Apples",
        "price": 2.99,
        "quantity": 2,
        "subtotal": 5.98
      }
    ],
    "total_price": 5.98,
    "status": "pending",
    "order_date": "2024-01-15T10:30:00Z",
    "delivery_address": "123 Main St, City, State 12345",
    "contact_phone": "555-1234"
  }
}
```

## Data Models

### Product Model
```json
{
  "_id": "ObjectId",
  "name": "string",
  "category": "string",
  "price": "number",
  "stock": "number",
  "description": "string"
}
```

### Cart Item Model
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "item_id": "ObjectId",
  "quantity": "number",
  "added_at": "ISO 8601 datetime"
}
```

### Order Model
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "items": [
    {
      "item_id": "ObjectId",
      "name": "string",
      "price": "number",
      "quantity": "number",
      "subtotal": "number"
    }
  ],
  "total_price": "number",
  "status": "string",
  "order_date": "ISO 8601 datetime",
  "delivery_address": "string",
  "contact_phone": "string"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

## Common Error Responses

### Item Not Found
```json
{
  "success": false,
  "error": "Item not found",
  "code": 404
}
```

### Invalid Request
```json
{
  "success": false,
  "error": "Missing required fields",
  "code": 400
}
```

### Empty Cart
```json
{
  "success": false,
  "error": "Cart is empty",
  "code": 400
}
```

## Sample Data

The API comes with pre-loaded sample data:

### Categories
- Fruits
- Dairy
- Vegetables
- Meat
- Pantry

### Sample Products
- **Fruits**: Apples ($2.99), Bananas ($1.99), Oranges ($3.49), Strawberries ($4.99)
- **Dairy**: Milk ($3.99), Cheese ($5.99), Yogurt ($1.49), Butter ($4.49)
- **Vegetables**: Carrots ($2.49), Broccoli ($3.99), Tomatoes ($2.99), Lettuce ($2.49)
- **Meat**: Chicken Breast ($7.99), Ground Beef ($6.99), Salmon ($12.99)
- **Pantry**: Rice ($4.99), Pasta ($2.99), Olive Oil ($8.99)

## Testing

### Using curl
```bash
# Test products endpoint
curl http://localhost:5000/items

# Test categories endpoint
curl http://localhost:5000/categories

# Test cart endpoint
curl http://localhost:5000/cart/user123
```

### Using Postman
1. Import the base URL: `http://localhost:5000`
2. Create requests for each endpoint
3. Set Content-Type to `application/json` for POST requests
4. Use the sample request bodies provided above

## Rate Limiting

Currently, there are no rate limits implemented. Consider adding rate limiting in production:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

## CORS Configuration

The API is configured to accept cross-origin requests from any domain. In production, restrict to specific domains:

```python
from flask_cors import CORS

CORS(app, origins=['http://localhost:3000', 'https://yourdomain.com'])
```

## Security Considerations

1. **Authentication**: Implement JWT tokens for user authentication
2. **Input Validation**: Validate all input data
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **HTTPS**: Use HTTPS in production
5. **Environment Variables**: Store sensitive data in environment variables
6. **Database Security**: Use MongoDB authentication and authorization

## Future Enhancements

1. **User Management**: Add user registration and authentication
2. **Payment Integration**: Add payment processing
3. **Order Tracking**: Add order status updates
4. **Inventory Management**: Add stock level alerts
5. **Search Optimization**: Add full-text search capabilities
6. **Caching**: Implement Redis for caching
7. **Analytics**: Add order and product analytics

---

**For support, please contact the development team or create an issue in the project repository.**
