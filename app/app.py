"""
Application Flask principale pour l'API de livraison de pizzas
"""
from flask import Flask, request, jsonify
from app.models import Pizza, Order, Delivery


app = Flask(__name__)

# Stockage en mémoire (pour simplifier, à remplacer par une DB en production)
pizzas_store = {}
orders_store = {}
deliveries_store = {}


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de santé de l'API"""
    return jsonify({"status": "healthy", "message": "Pizza API is running"}), 200


# ==================== PIZZA ENDPOINTS ====================

@app.route('/pizzas', methods=['POST'])
def create_pizza():
    """Crée une nouvelle pizza"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['name', 'size', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        pizza = Pizza(
            name=data['name'],
            size=data['size'],
            price=data['price'],
            toppings=data.get('toppings', [])
        )
        
        pizza_id = str(len(pizzas_store) + 1)
        pizzas_store[pizza_id] = pizza
        
        result = pizza.to_dict()
        result['pizza_id'] = pizza_id
        
        return jsonify(result), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/pizzas/<pizza_id>', methods=['GET'])
def get_pizza(pizza_id):
    """Récupère une pizza par son ID"""
    if pizza_id not in pizzas_store:
        return jsonify({"error": "Pizza not found"}), 404
    
    pizza = pizzas_store[pizza_id]
    result = pizza.to_dict()
    result['pizza_id'] = pizza_id
    
    return jsonify(result), 200


@app.route('/pizzas', methods=['GET'])
def get_all_pizzas():
    """Récupère toutes les pizzas"""
    pizzas_list = []
    for pizza_id, pizza in pizzas_store.items():
        pizza_dict = pizza.to_dict()
        pizza_dict['pizza_id'] = pizza_id
        pizzas_list.append(pizza_dict)
    
    return jsonify({"pizzas": pizzas_list, "count": len(pizzas_list)}), 200


# ==================== ORDER ENDPOINTS ====================

@app.route('/orders', methods=['POST'])
def create_order():
    """Crée une nouvelle commande"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['customer_name', 'customer_address']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        order = Order(
            customer_name=data['customer_name'],
            customer_address=data['customer_address']
        )
        
        orders_store[order.order_id] = order
        
        return jsonify(order.to_dict()), 201
    
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Récupère une commande par son ID"""
    if order_id not in orders_store:
        return jsonify({"error": "Order not found"}), 404
    
    order = orders_store[order_id]
    return jsonify(order.to_dict()), 200


@app.route('/orders', methods=['GET'])
def get_all_orders():
    """Récupère toutes les commandes"""
    orders_list = [order.to_dict() for order in orders_store.values()]
    return jsonify({"orders": orders_list, "count": len(orders_list)}), 200


@app.route('/orders/<order_id>/pizzas', methods=['POST'])
def add_pizza_to_order(order_id):
    """Ajoute une pizza à une commande"""
    if order_id not in orders_store:
        return jsonify({"error": "Order not found"}), 404
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Option 1: Créer une nouvelle pizza directement
        if 'name' in data and 'size' in data and 'price' in data:
            pizza = Pizza(
                name=data['name'],
                size=data['size'],
                price=data['price'],
                toppings=data.get('toppings', [])
            )
        # Option 2: Utiliser une pizza existante par son ID
        elif 'pizza_id' in data:
            pizza_id = data['pizza_id']
            if pizza_id not in pizzas_store:
                return jsonify({"error": "Pizza not found"}), 404
            pizza = pizzas_store[pizza_id]
        else:
            return jsonify({"error": "Invalid pizza data"}), 400
        
        order = orders_store[order_id]
        order.add_pizza(pizza)
        
        return jsonify(order.to_dict()), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/orders/<order_id>/pizzas/<int:pizza_index>', methods=['DELETE'])
def remove_pizza_from_order(order_id, pizza_index):
    """Retire une pizza d'une commande"""
    if order_id not in orders_store:
        return jsonify({"error": "Order not found"}), 404
    
    order = orders_store[order_id]
    
    if pizza_index < 0 or pizza_index >= len(order.pizzas):
        return jsonify({"error": "Invalid pizza index"}), 400
    
    order.remove_pizza(pizza_index)
    
    return jsonify(order.to_dict()), 200


@app.route('/orders/<order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    """Met à jour le statut d'une commande"""
    if order_id not in orders_store:
        return jsonify({"error": "Order not found"}), 404
    
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({"error": "Status is required"}), 400
        
        order = orders_store[order_id]
        order.update_status(data['status'])
        
        return jsonify(order.to_dict()), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# ==================== DELIVERY ENDPOINTS ====================

@app.route('/deliveries', methods=['POST'])
def create_delivery():
    """Crée une nouvelle livraison"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['order_id', 'driver_name']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        order_id = data['order_id']
        if order_id not in orders_store:
            return jsonify({"error": "Order not found"}), 404
        
        order = orders_store[order_id]
        
        delivery = Delivery(
            order=order,
            driver_name=data['driver_name']
        )
        
        deliveries_store[delivery.delivery_id] = delivery
        
        return jsonify(delivery.to_dict()), 201
    
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/deliveries/<delivery_id>', methods=['GET'])
def get_delivery(delivery_id):
    """Récupère une livraison par son ID"""
    if delivery_id not in deliveries_store:
        return jsonify({"error": "Delivery not found"}), 404
    
    delivery = deliveries_store[delivery_id]
    return jsonify(delivery.to_dict()), 200


@app.route('/deliveries', methods=['GET'])
def get_all_deliveries():
    """Récupère toutes les livraisons"""
    deliveries_list = [delivery.to_dict() for delivery in deliveries_store.values()]
    return jsonify({"deliveries": deliveries_list, "count": len(deliveries_list)}), 200


@app.route('/deliveries/<delivery_id>/start', methods=['PATCH'])
def start_delivery(delivery_id):
    """Démarre une livraison"""
    if delivery_id not in deliveries_store:
        return jsonify({"error": "Delivery not found"}), 404
    
    try:
        delivery = deliveries_store[delivery_id]
        delivery.start_delivery()
        
        return jsonify(delivery.to_dict()), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/deliveries/<delivery_id>/complete', methods=['PATCH'])
def complete_delivery(delivery_id):
    """Complète une livraison"""
    if delivery_id not in deliveries_store:
        return jsonify({"error": "Delivery not found"}), 404
    
    try:
        delivery = deliveries_store[delivery_id]
        delivery.complete_delivery()
        
        return jsonify(delivery.to_dict()), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/deliveries/<delivery_id>/location', methods=['PATCH'])
def update_delivery_location(delivery_id):
    """Met à jour la position GPS du livreur"""
    if delivery_id not in deliveries_store:
        return jsonify({"error": "Delivery not found"}), 404
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        delivery = deliveries_store[delivery_id]
        delivery.update_location(
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        
        return jsonify(delivery.to_dict()), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/deliveries/<delivery_id>/cancel', methods=['PATCH'])
def cancel_delivery(delivery_id):
    """Annule une livraison"""
    if delivery_id not in deliveries_store:
        return jsonify({"error": "Delivery not found"}), 404
    
    try:
        data = request.get_json()
        
        if not data or 'reason' not in data:
            return jsonify({"error": "Cancellation reason is required"}), 400
        
        delivery = deliveries_store[delivery_id]
        delivery.cancel_delivery(data['reason'])
        
        return jsonify(delivery.to_dict()), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handler pour les erreurs 404"""
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler pour les erreurs 500"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
