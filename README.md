# Pika-Light

# 🛒 PIKA-LIGHT Grocery Delivery

A full-stack grocery delivery application with a RESTful API backend and responsive web frontend.

![PIKA-LIGHT Demo](https://img.shields.io/badge/Status-Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-red)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green)

##  Table of Contents

* [Features](#features)
* [Tech Stack](#tech-stack)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [API Documentation](#api-documentation)
* [Frontend Features](#frontend-features)
* [Database Schema](#database-schema)
* [Testing](#testing)
* [Contributing](#contributing)
  

## Features

### Backend (API)

* Product Catalog: Browse products by category
* Search & Filter: Search products by name or category
* Shopping Cart: Add, remove, update items
* Order Management: Place orders and view history
* Stock Management: Real-time inventory
* Data Validation & Error Handling
* RESTful API

### Frontend (Web App)

* Responsive Design for all devices
* Modern UI with animations
* Real-time Cart Updates
* Simple Checkout
* Live Updates
* Fast Performance

##  Tech Stack

**Backend:**

* Python 3.8+
* Flask 2.3.3
* MongoDB
* Flask-CORS, PyMongo, BSON

**Frontend:**

* HTML5, CSS3, JavaScript (ES6+)
* Responsive design

##  Project Structure

```
pika-light/

│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   └── pika.html
├── docs/
│   └── api_documentation.md
└── README.md
```

##  Installation

### Prerequisites

* Python 3.8+
* MongoDB
* Modern browser

### Backend Setup

```bash
git clone <repository-url>
cd pika-light
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

### Frontend Setup

* Open `frontend/index.html` in a browser
* Optionally serve using:

```bash
cd frontend
python -m http.server 8000
```

##  Usage

1. Start MongoDB
2. Run backend: `python app.py`
3. Open frontend in browser
4. Start shopping

###  Data

Includes Fruits, Dairy, Vegetables, Meat, Pantry items.

### User Flow

* Browse -> Add to cart -> Checkout -> Confirm order

##  API Documentation

**Base URL:** `http://localhost:5000`

### Endpoints

**Products:**

* GET /items
* GET /items?category=Fruits
* GET /items?search=apple
* GET /items/<id>
* GET /categories

**Cart:**

* POST /cart
* GET /cart/\<user\_id>
* DELETE /cart/\<user\_id>/\<item\_id>
* DELETE /cart/\<user\_id>

**Orders:**

* POST /orders
* GET /orders/\<user\_id>
* GET /orders/\<user\_id>/\<order\_id>

##  Frontend Features

* Responsive: Desktop, Tablet, Mobile
* Clean UI
* Smooth Animations
* Real-time Cart
* Search & Filter
* Checkout modal

##  Database Schema

**Items:**

```json
{
  "_id": "ObjectId",
  "name": "Product Name",
  "category": "Category",
  "price": 9.99,
  "stock": 25,
  "description": "Product description"
}
```

**Cart:**

```json
{
  "_id": "ObjectId",
  "user_id": "user123",
  "item_id": "item_object_id",
  "quantity": 2,
  "added_at": "2024-01-15T10:30:00Z"
}
```

**Orders:**

```json
{
  "_id": "ObjectId",
  "user_id": "user123",
  "items": [...],
  "total_price": 19.98,
  "status": "pending",
  "order_date": "2024-01-15T10:30:00Z",
  "delivery_address": "123 Main St",
  "contact_phone": "555-1234"
}
```

##  Testing

Backend:

```bash
curl http://localhost:5000/items
```

Frontend:

* Browser DevTools
* Test all features manually

##  Development

* Add new backend routes in `app.py`
* Update frontend JavaScript
* Modify database schemas as needed

Environment Variables:

```bash
MONGODB_URI=mongodb://localhost:27017/
FLASK_ENV=production
SECRET_KEY=your-secret-key
```

##  Deployment

* Use environment variables
* Reverse proxy (nginx)
* Gunicorn for Flask
* SSL setup

Docker (Optional) You can use it locally:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

##  Contributing

1. Fork
2. Branch
3. Commit
4. Push
5. PR

Guidelines:

* Follow PEP 8
* Write clear commits
* Add tests


##  Support

* Email: [benaiahraini@pika-light.com](mailto:benaiahraini@pika-light.com)
* GitHub Issues
* Wiki

---

Made with care by the PIKA-LIGHT .

Happy Shopping!
