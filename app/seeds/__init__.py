"""
Module de peuplement de la base de données
Fonctions pour insérer les données de démonstration
"""
from datetime import datetime, timedelta
import json
from app.database import db
from app.models.db_models import PizzaDB, OrderDB, OrderPizzaDB, DeliveryDB
from app.seeds.catalog import CATALOG_PIZZAS, SAMPLE_ORDERS


def seed_pizzas():
    """
    Peuple la base avec le catalogue de pizzas

    Returns:
        int: Nombre de pizzas ajoutées
    """
    print("🍕 Ajout du catalogue de pizzas...")

    count = 0
    for pizza_data in CATALOG_PIZZAS:
        # Convertir la liste de toppings en JSON
        pizza = PizzaDB(
            name=pizza_data['name'],
            size=pizza_data['size'],
            price_amount=pizza_data['price_amount'],
            price_currency=pizza_data['price_currency'],
            toppings=json.dumps(pizza_data['toppings'])
        )
        db.session.add(pizza)
        count += 1

    db.session.commit()
    print(f"   ✅ {count} pizzas ajoutées")
    return count


def seed_orders():
    """
    Peuple la base avec des exemples de commandes

    Returns:
        int: Nombre de commandes ajoutées
    """
    print("📦 Ajout d'exemples de commandes...")

    # Récupérer toutes les pizzas du catalogue
    pizzas = PizzaDB.query.all()

    if not pizzas:
        print("   ⚠️  Aucune pizza trouvée. Impossible d'ajouter des commandes.")
        return 0

    count = 0
    for order_data in SAMPLE_ORDERS:
        # Calculer la date de création
        created_at = datetime.now()
        if order_data.get('delivery'):
            if 'days_ago' in order_data['delivery']:
                created_at = datetime.now() - timedelta(days=order_data['delivery']['days_ago'])
            elif 'hours_ago' in order_data['delivery']:
                created_at = datetime.now() - timedelta(hours=order_data['delivery']['hours_ago'])
            elif 'minutes_ago' in order_data['delivery']:
                created_at = datetime.now() - timedelta(minutes=order_data['delivery']['minutes_ago'])

        # Créer la commande
        order = OrderDB(
            customer_name=order_data['customer_name'],
            customer_address=order_data['customer_address'],
            status=order_data['status'],
            created_at=created_at
        )
        db.session.add(order)
        db.session.flush()  # Pour obtenir l'ID

        # Ajouter les pizzas à la commande
        for pizza_idx in order_data['pizzas_indices']:
            if pizza_idx < len(pizzas):
                order_pizza = OrderPizzaDB(
                    order_id=order.id,
                    pizza_id=pizzas[pizza_idx].id
                )
                db.session.add(order_pizza)

        # Créer la livraison si nécessaire
        if order_data.get('delivery'):
            delivery_info = order_data['delivery']
            delivery = DeliveryDB(
                order_id=order.id,
                driver_name=delivery_info['driver_name'],
                status=delivery_info['status']
            )

            # Ajouter les dates selon le statut
            if delivery_info['status'] in ['in_transit', 'delivered']:
                if 'hours_ago' in delivery_info:
                    delivery.started_at = datetime.now() - timedelta(hours=delivery_info['hours_ago'], minutes=10)
                elif 'days_ago' in delivery_info:
                    delivery.started_at = datetime.now() - timedelta(days=delivery_info['days_ago'], hours=1)

            if delivery_info['status'] == 'delivered':
                if 'days_ago' in delivery_info:
                    delivery.completed_at = datetime.now() - timedelta(days=delivery_info['days_ago'])

            db.session.add(delivery)

        count += 1

    db.session.commit()
    print(f"   ✅ {count} commandes ajoutées")
    return count


def seed_all():
    """
    Peuple toute la base de données avec les données de démonstration

    Returns:
        dict: Statistiques du peuplement
    """
    pizzas_count = seed_pizzas()
    orders_count = seed_orders()

    return {
        'pizzas': pizzas_count,
        'orders': orders_count
    }


def is_database_empty():
    """
    Vérifie si la base de données est vide

    Returns:
        bool: True si la base est vide, False sinon
    """
    pizzas_count = PizzaDB.query.count()
    orders_count = OrderDB.query.count()
    return pizzas_count == 0 and orders_count == 0

