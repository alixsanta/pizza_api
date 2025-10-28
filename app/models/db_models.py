"""
Modèles SQLAlchemy pour la persistance en base de données
"""
from app.database import db
from datetime import datetime
import uuid
import json


class PizzaDB(db.Model):
    """Modèle de base de données pour Pizza"""
    __tablename__ = 'pizzas'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    price_amount = db.Column(db.Float, nullable=False)
    price_currency = db.Column(db.String(3), default='EUR')
    toppings = db.Column(db.Text, default='[]')  # Stocké en JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation avec les commandes (many-to-many)
    orders = db.relationship('OrderPizzaDB', back_populates='pizza', cascade='all, delete-orphan')

    def to_dict(self):
        """Convertit le modèle DB en dictionnaire"""
        return {
            'pizza_id': self.id,
            'name': self.name,
            'size': self.size,
            'price': self.price_amount,
            'currency': self.price_currency,
            'toppings': json.loads(self.toppings) if self.toppings else []
        }

    @staticmethod
    def from_pizza_object(pizza, pizza_id=None):
        """Crée un PizzaDB à partir d'un objet Pizza"""
        return PizzaDB(
            id=pizza_id or str(uuid.uuid4()),
            name=pizza.name,
            size=pizza.size,
            price_amount=pizza.price.amount,
            price_currency=pizza.price.currency,
            toppings=json.dumps(pizza.toppings)
        )


class OrderDB(db.Model):
    """Modèle de base de données pour Order"""
    __tablename__ = 'orders'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_name = db.Column(db.String(100), nullable=False)
    customer_address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    pizzas = db.relationship('OrderPizzaDB', back_populates='order', cascade='all, delete-orphan')
    delivery = db.relationship('DeliveryDB', back_populates='order', uselist=False, cascade='all, delete-orphan')

    def to_dict(self, include_pizzas=True):
        """Convertit le modèle DB en dictionnaire"""
        from app.models import Pizza, Price, Order

        result = {
            'order_id': self.id,
            'customer_name': self.customer_name,
            'customer_address': self.customer_address,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

        if include_pizzas:
            pizzas_list = []
            total_amount = 0
            currency = 'EUR'

            for order_pizza in self.pizzas:
                pizza_dict = order_pizza.pizza.to_dict()
                del pizza_dict['pizza_id']  # Enlever l'ID pour la compatibilité
                pizzas_list.append(pizza_dict)
                total_amount += order_pizza.pizza.price_amount
                currency = order_pizza.pizza.price_currency

            result['pizzas'] = pizzas_list
            result['total'] = round(total_amount, 2)
            result['currency'] = currency
            result['is_valid'] = len(pizzas_list) > 0

        return result

    @staticmethod
    def from_order_object(order):
        """Crée un OrderDB à partir d'un objet Order"""
        return OrderDB(
            id=order.order_id,
            customer_name=order.customer_name,
            customer_address=order.customer_address,
            status=order.status,
            created_at=order.created_at
        )


class OrderPizzaDB(db.Model):
    """Table de liaison entre Order et Pizza (many-to-many)"""
    __tablename__ = 'order_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    pizza_id = db.Column(db.String(36), db.ForeignKey('pizzas.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    order = db.relationship('OrderDB', back_populates='pizzas')
    pizza = db.relationship('PizzaDB', back_populates='orders')


class DeliveryDB(db.Model):
    """Modèle de base de données pour Delivery"""
    __tablename__ = 'deliveries'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False, unique=True)
    driver_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='assigned')
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    current_latitude = db.Column(db.Float, nullable=True)
    current_longitude = db.Column(db.Float, nullable=True)
    cancellation_reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation
    order = db.relationship('OrderDB', back_populates='delivery')

    def to_dict(self):
        """Convertit le modèle DB en dictionnaire"""
        return {
            'delivery_id': self.id,
            'order': self.order.to_dict() if self.order else None,
            'driver_name': self.driver_name,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'current_latitude': self.current_latitude,
            'current_longitude': self.current_longitude,
            'cancellation_reason': self.cancellation_reason
        }

    @staticmethod
    def from_delivery_object(delivery):
        """Crée un DeliveryDB à partir d'un objet Delivery"""
        return DeliveryDB(
            id=delivery.delivery_id,
            order_id=delivery.order.order_id,
            driver_name=delivery.driver_name,
            status=delivery.status,
            started_at=delivery.started_at,
            completed_at=delivery.completed_at,
            current_latitude=delivery.current_latitude,
            current_longitude=delivery.current_longitude,
            cancellation_reason=delivery.cancellation_reason
        )

