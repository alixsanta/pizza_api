"""
Application Flask principale pour l'API de livraison de pizzas
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from app.models import Pizza, Order, Delivery
from app.database import db, init_db
from app.models.db_models import PizzaDB, OrderDB, OrderPizzaDB, DeliveryDB
from datetime import datetime
import os


app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

# Configuration de la base de données SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'pizza_delivery.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Activer CORS pour permettre les requêtes depuis le navigateur
CORS(app)

# Initialiser la base de données
init_db(app)


# ==================== WEB INTERFACE ====================

@app.route('/')
def index():
    """Page d'accueil de l'application web de commande"""
    return render_template('index.html')


# ==================== HEALTH CHECK ====================

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
        
        # Créer l'objet Pizza pour validation
        pizza = Pizza(
            name=data['name'],
            size=data['size'],
            price=data['price'],
            toppings=data.get('toppings', [])
        )
        
        # Sauvegarder dans la base de données
        pizza_db = PizzaDB.from_pizza_object(pizza)
        db.session.add(pizza_db)
        db.session.commit()

        return jsonify(pizza_db.to_dict()), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route('/pizzas/<pizza_id>', methods=['GET'])
def get_pizza(pizza_id):
    """Récupère une pizza par son ID"""
    pizza_db = PizzaDB.query.get(pizza_id)

    if not pizza_db:
        return jsonify({"error": "Pizza not found"}), 404
    
    return jsonify(pizza_db.to_dict()), 200


@app.route('/pizzas', methods=['GET'])
def get_all_pizzas():
    """Récupère toutes les pizzas"""
    pizzas_db = PizzaDB.query.all()
    pizzas_list = [pizza.to_dict() for pizza in pizzas_db]

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
        
        # Sauvegarder dans la base de données
        order_db = OrderDB.from_order_object(order)
        db.session.add(order_db)
        db.session.commit()

        return jsonify(order_db.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Récupère une commande par son ID"""
    order_db = OrderDB.query.get(order_id)

    if not order_db:
        return jsonify({"error": "Order not found"}), 404
    
    return jsonify(order_db.to_dict()), 200


@app.route('/orders', methods=['GET'])
def get_all_orders():
    """Récupère toutes les commandes"""
    orders_db = OrderDB.query.all()
    orders_list = [order.to_dict() for order in orders_db]

    return jsonify({"orders": orders_list, "count": len(orders_list)}), 200


@app.route('/orders/<order_id>/pizzas', methods=['POST'])
def add_pizza_to_order(order_id):
    """Ajoute une pizza à une commande"""
    order_db = OrderDB.query.get(order_id)

    if not order_db:
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
            pizza_db = PizzaDB.from_pizza_object(pizza)
            db.session.add(pizza_db)
            db.session.flush()  # Pour obtenir l'ID

        # Option 2: Utiliser une pizza existante par son ID
        elif 'pizza_id' in data:
            pizza_id = data['pizza_id']
            pizza_db = PizzaDB.query.get(pizza_id)
            if not pizza_db:
                return jsonify({"error": "Pizza not found"}), 404
        else:
            return jsonify({"error": "Invalid pizza data"}), 400
        
        # Créer la liaison
        order_pizza = OrderPizzaDB(order_id=order_id, pizza_id=pizza_db.id)
        db.session.add(order_pizza)
        db.session.commit()

        return jsonify(order_db.to_dict()), 200

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route('/orders/<order_id>/pizzas/<int:pizza_index>', methods=['DELETE'])
def remove_pizza_from_order(order_id, pizza_index):
    """Retire une pizza d'une commande"""
    order_db = OrderDB.query.get(order_id)

    if not order_db:
        return jsonify({"error": "Order not found"}), 404
    
    if pizza_index < 0 or pizza_index >= len(order_db.pizzas):
        return jsonify({"error": "Invalid pizza index"}), 400
    
    # Supprimer la liaison à l'index spécifié
    order_pizza_to_remove = order_db.pizzas[pizza_index]
    db.session.delete(order_pizza_to_remove)
    db.session.commit()

    return jsonify(order_db.to_dict()), 200


@app.route('/orders/<order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    """Met à jour le statut d'une commande"""
    order_db = OrderDB.query.get(order_id)

    if not order_db:
        return jsonify({"error": "Order not found"}), 404
    
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({"error": "Status is required"}), 400
        
        # Valider le statut
        valid_statuses = ["pending", "preparing", "ready", "out_for_delivery", "delivered", "cancelled"]
        if data['status'] not in valid_statuses:
            return jsonify({"error": f"Invalid status. Must be one of {valid_statuses}"}), 400

        # Valider que la commande a au moins une pizza pour certains statuts
        if data['status'] in ["preparing", "ready", "out_for_delivery", "delivered"]:
            if len(order_db.pizzas) == 0:
                return jsonify({"error": "Order must have at least one pizza to be valid"}), 400

        order_db.status = data['status']
        db.session.commit()

        return jsonify(order_db.to_dict()), 200

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
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
        order_db = OrderDB.query.get(order_id)

        if not order_db:
            return jsonify({"error": "Order not found"}), 404
        
        # Vérifier si une livraison existe déjà pour cette commande
        existing_delivery = DeliveryDB.query.filter_by(order_id=order_id).first()
        if existing_delivery:
            return jsonify({"error": "Delivery already exists for this order"}), 400

        # Créer la livraison
        delivery_db = DeliveryDB(
            order_id=order_id,
            driver_name=data['driver_name']
        )
        
        db.session.add(delivery_db)
        db.session.commit()

        return jsonify(delivery_db.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route('/deliveries/<delivery_id>', methods=['GET'])
def get_delivery(delivery_id):
    """Récupère une livraison par son ID"""
    delivery_db = DeliveryDB.query.get(delivery_id)

    if not delivery_db:
        return jsonify({"error": "Delivery not found"}), 404
    
    return jsonify(delivery_db.to_dict()), 200


@app.route('/deliveries', methods=['GET'])
def get_all_deliveries():
    """Récupère toutes les livraisons"""
    deliveries_db = DeliveryDB.query.all()
    deliveries_list = [delivery.to_dict() for delivery in deliveries_db]

    return jsonify({"deliveries": deliveries_list, "count": len(deliveries_list)}), 200


@app.route('/deliveries/<delivery_id>/start', methods=['PATCH'])
def start_delivery(delivery_id):
    """Démarre une livraison"""
    delivery_db = DeliveryDB.query.get(delivery_id)

    if not delivery_db:
        return jsonify({"error": "Delivery not found"}), 404
    
    try:
        # Validation des statuts
        if delivery_db.status == "in_transit":
            return jsonify({"error": "Delivery has already been started"}), 400

        if delivery_db.status == "delivered":
            return jsonify({"error": "Delivery has already been completed"}), 400

        if delivery_db.status == "cancelled":
            return jsonify({"error": "Cannot start a cancelled delivery"}), 400

        # Mettre à jour le statut
        delivery_db.status = "in_transit"
        delivery_db.started_at = datetime.utcnow()
        db.session.commit()

        return jsonify(delivery_db.to_dict()), 200

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route('/deliveries/<delivery_id>/complete', methods=['PATCH'])
def complete_delivery(delivery_id):
    """Complète une livraison"""
    delivery_db = DeliveryDB.query.get(delivery_id)

    if not delivery_db:
        return jsonify({"error": "Delivery not found"}), 404
    
    try:
        # Validation du statut
        if delivery_db.status != "in_transit":
            return jsonify({"error": "Delivery must be started before it can be completed"}), 400

        # Mettre à jour le statut
        delivery_db.status = "delivered"
        delivery_db.completed_at = datetime.utcnow()
        db.session.commit()

        return jsonify(delivery_db.to_dict()), 200

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route('/deliveries/<delivery_id>/location', methods=['PATCH'])
def update_delivery_location(delivery_id):
    """Met à jour la position GPS du livreur"""
    delivery_db = DeliveryDB.query.get(delivery_id)

    if not delivery_db:
        return jsonify({"error": "Delivery not found"}), 404
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Mettre à jour la position
        delivery_db.current_latitude = data['latitude']
        delivery_db.current_longitude = data['longitude']
        db.session.commit()

        return jsonify(delivery_db.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route('/deliveries/<delivery_id>/cancel', methods=['PATCH'])
def cancel_delivery(delivery_id):
    """Annule une livraison"""
    delivery_db = DeliveryDB.query.get(delivery_id)

    if not delivery_db:
        return jsonify({"error": "Delivery not found"}), 404
    
    try:
        data = request.get_json()
        
        if not data or 'reason' not in data:
            return jsonify({"error": "Cancellation reason is required"}), 400
        
        # Annuler la livraison
        delivery_db.status = "cancelled"
        delivery_db.cancellation_reason = data['reason']
        db.session.commit()

        return jsonify(delivery_db.to_dict()), 200

    except Exception as e:
        db.session.rollback()
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
