import requests
from twilio.rest import Client
from flask import request, jsonify
from app import app, db
from models import User, Product, Order, OrderItem

BARCODE_LOOKUP_API_KEY = 'https://api.barcodelookup.com/v3/products?barcode=978014015737&formatted=y&key=ifDzhmKslKav42OD93NE'

TWILIO_ACCOUNT_SID = 'ACcc5b230b6a34fce88ef59b27c7caa515'
TWILIO_AUTH_TOKEN = 'f0847b9c21a10b0e5c0384caec14feaf'
TWILIO_PHONE_NUMBER = '+18667859763'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def get_object_or_404(model, id):
    obj = model.query.get(id)
    if obj is None:
        return jsonify({'error': f'{model.__name__} not found'}), 404
    return obj

@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'], 
            role=data.get('role', 'staff')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    elif request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

@app.route('/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    user = get_object_or_404(User, user_id)
    if isinstance(user, tuple):
        return user  

    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        user.username = data['username']
        user.email = data['email']
        user.password = data['password'] 
        user.role = data.get('role', user.role)
        db.session.commit()
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'})

@app.route('/api/products', methods=['GET', 'POST'])
def handle_products():
    if request.method == 'POST':
        data = request.get_json()
        new_product = Product(
            name=data['name'],
            description=data['description'],
            sku=data['sku'],
            price=data['price'],
            inventory_level=data['inventory_level']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201
    elif request.method == 'GET':
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products])

@app.route('/api/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_product(product_id):
    product = get_object_or_404(Product, product_id)
    if isinstance(product, tuple):
        return product  
    
    if request.method == 'GET':
        return jsonify(product.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        product.name = data['name']
        product.description = data['description']
        product.sku = data['sku']
        product.price = data['price']
        product.inventory_level = data['inventory_level']
        db.session.commit()
        return jsonify(product.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'})

@app.route('/api/orders', methods=['GET', 'POST'])
def handle_orders():
    if request.method == 'POST':
        data = request.get_json()
        new_order = Order(
            total_amount=data['total_amount'],
            status=data.get('status', 'Pending')
        )
        db.session.add(new_order)
        db.session.commit()

        for item in data['order_items']:
            order_item = OrderItem(
                product_id=item['product_id'],
                order_id=new_order.id,
                quantity=item['quantity']
            )
            db.session.add(order_item)

        db.session.commit()
        return jsonify(new_order.to_dict()), 201
    elif request.method == 'GET':
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders])

@app.route('/api/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_order(order_id):
    order = get_object_or_404(Order, order_id)
    if isinstance(order, tuple):
        return order  

    if request.method == 'GET':
        return jsonify(order.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        order.total_amount = data['total_amount']
        order.status = data.get('status', order.status)
        db.session.commit()
        return jsonify(order.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted'})

# Barcode Lookup API Integration
@app.route('/api/barcode/<barcode>', methods=['GET'])
def lookup_barcode(barcode):
    url = f'https://api.barcodelookup.com/v2/products?barcode={barcode}&formatted=y&key={BARCODE_LOOKUP_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['products']:
            product_info = data['products'][0]
            return jsonify({
                'name': product_info.get('product_name', ''),
                'description': product_info.get('description', ''),
                'sku': product_info.get('barcode_number', ''),
                'price': product_info.get('price', ''),
                'inventory_level': 0  
            })
        else:
            return jsonify({'error': 'Product not found'}), 404
    else:
        return jsonify({'error': 'Failed to fetch data from Barcode Lookup API'}), 500

@app.route('/api/notify', methods=['POST'])
def send_notification():
    data = request.get_json()
    message_body = data['message']
    to_phone_number = data['to']

    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        return jsonify({'sid': message.sid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
