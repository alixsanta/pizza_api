"""
Exemple d'utilisation de l'API Pizza Delivery avec la classe Price
"""
from app.models import Price, Pizza, Order, Delivery


def main():
    print("🍕 Démonstration de l'API Pizza Delivery\n")
    print("=" * 60)
    
    # ===== 1. Création de prix avec Price =====
    print("\n1️⃣  Création de prix avec Price")
    print("-" * 60)
    
    price1 = Price(amount=12.99, currency="EUR")
    price2 = Price(amount=15.99, currency="EUR")
    
    print(f"Prix 1: {price1.format(with_symbol=True)}")
    print(f"Prix 2: {price2.format(with_symbol=True)}")
    
    # Addition
    total = price1 + price2
    print(f"Total: {total.format(with_symbol=True)}")
    
    # Réduction
    discounted = price2.apply_discount(10)  # 10% de réduction
    print(f"Prix 2 avec 10% de réduction: {discounted.format(with_symbol=True)}")
    
    # Taxe
    with_tax = price1.apply_tax(20)  # TVA 20%
    print(f"Prix 1 avec TVA 20%: {with_tax.format(with_symbol=True)}")
    
    # ===== 2. Création de pizzas =====
    print("\n2️⃣  Création de pizzas")
    print("-" * 60)
    
    # Avec un float (converti automatiquement en Price)
    pizza1 = Pizza(
        name="Margherita",
        size="Medium",
        price=12.99,
        toppings=["tomato", "mozzarella", "basil"]
    )
    
    # Avec un objet Price
    pizza2 = Pizza(
        name="Pepperoni",
        size="Large",
        price=Price(amount=15.99, currency="EUR"),
        toppings=["pepperoni", "cheese"]
    )
    
    pizza3 = Pizza(
        name="Supreme",
        size="Large",
        price=18.99,
        toppings=["pepperoni", "mushrooms", "olives", "peppers"]
    )
    
    print(f"✅ {pizza1.name}: {pizza1.price.format(with_symbol=True)}")
    print(f"✅ {pizza2.name}: {pizza2.price.format(with_symbol=True)}")
    print(f"✅ {pizza3.name}: {pizza3.price.format(with_symbol=True)}")
    
    # ===== 3. Création d'une commande =====
    print("\n3️⃣  Création d'une commande")
    print("-" * 60)
    
    order = Order(
        customer_name="John Doe",
        customer_address="123 Main Street"
    )
    
    print(f"Commande créée: {order.order_id}")
    print(f"Client: {order.customer_name}")
    print(f"Adresse: {order.customer_address}")
    print(f"Statut: {order.status}")
    print(f"Valide: {order.is_valid()} ❌ (pas de pizza)")
    
    # ===== 4. Ajout de pizzas à la commande =====
    print("\n4️⃣  Ajout de pizzas à la commande")
    print("-" * 60)
    
    order.add_pizza(pizza1)
    print(f"✅ Pizza ajoutée: {pizza1.name}")
    print(f"Valide: {order.is_valid()} ✅")
    
    order.add_pizza(pizza2)
    print(f"✅ Pizza ajoutée: {pizza2.name}")
    
    order.add_pizza(pizza3)
    print(f"✅ Pizza ajoutée: {pizza3.name}")
    
    # ===== 5. Calcul du total =====
    print("\n5️⃣  Calcul du total")
    print("-" * 60)
    
    total_price = order.calculate_total()
    print(f"Nombre de pizzas: {len(order.pizzas)}")
    print(f"Total: {total_price.format(with_symbol=True)}")
    print(f"Total HT: {total_price.format(with_symbol=True)}")
    
    # Appliquer une réduction de 10%
    total_with_discount = total_price.apply_discount(10)
    print(f"Total avec 10% de réduction: {total_with_discount.format(with_symbol=True)}")
    
    # Appliquer la TVA
    total_ttc = total_with_discount.apply_tax(20)
    print(f"Total TTC (avec TVA 20%): {total_ttc.format(with_symbol=True)}")
    
    # ===== 6. Validation de la commande =====
    print("\n6️⃣  Validation et changement de statut")
    print("-" * 60)
    
    try:
        order.validate()
        print("✅ Commande validée (a au moins une pizza)")
    except ValueError as e:
        print(f"❌ Erreur de validation: {e}")
    
    # Changer de statut (nécessite une validation)
    order.update_status("preparing")
    print(f"Statut mis à jour: {order.status}")
    
    order.update_status("ready")
    print(f"Statut mis à jour: {order.status}")
    
    # ===== 7. Test de validation d'une commande vide =====
    print("\n7️⃣  Test de validation d'une commande vide")
    print("-" * 60)
    
    empty_order = Order(
        customer_name="Jane Smith",
        customer_address="456 Oak Avenue"
    )
    
    print(f"Commande vide créée: {empty_order.order_id}")
    print(f"Valide: {empty_order.is_valid()} ❌")
    
    try:
        empty_order.validate()
        print("✅ Commande validée")
    except ValueError as e:
        print(f"❌ Erreur de validation: {e}")
    
    try:
        empty_order.update_status("preparing")
        print("✅ Statut changé à preparing")
    except ValueError as e:
        print(f"❌ Impossible de changer le statut: {e}")
    
    # ===== 8. Création d'une livraison =====
    print("\n8️⃣  Création d'une livraison")
    print("-" * 60)
    
    delivery = Delivery(
        order=order,
        driver_name="Mike Driver"
    )
    
    print(f"Livraison créée: {delivery.delivery_id}")
    print(f"Livreur: {delivery.driver_name}")
    print(f"Statut: {delivery.status}")
    print(f"Commande: {delivery.order.order_id}")
    print(f"Total de la commande: {delivery.order.calculate_total().format(with_symbol=True)}")
    
    # Démarrer la livraison
    delivery.start_delivery()
    print(f"\n🚚 Livraison démarrée")
    print(f"Statut: {delivery.status}")
    
    # Mettre à jour la position
    delivery.update_location(latitude=48.8566, longitude=2.3522)
    print(f"📍 Position mise à jour: {delivery.current_latitude}, {delivery.current_longitude}")
    
    # Compléter la livraison
    delivery.complete_delivery()
    print(f"\n✅ Livraison terminée")
    print(f"Statut: {delivery.status}")
    
    duration = delivery.calculate_duration()
    print(f"Durée: {duration:.2f} secondes")
    
    # ===== 9. Résumé final =====
    print("\n9️⃣  Résumé final")
    print("=" * 60)
    
    order_dict = order.to_dict()
    print(f"Commande: {order_dict['order_id']}")
    print(f"Client: {order_dict['customer_name']}")
    print(f"Nombre de pizzas: {len(order_dict['pizzas'])}")
    print(f"Total: {order_dict['total']:.2f} {order_dict['currency']}")
    print(f"Statut: {order_dict['status']}")
    print(f"Valide: {order_dict['is_valid']}")
    
    print("\nPizzas commandées:")
    for i, pizza_dict in enumerate(order_dict['pizzas'], 1):
        print(f"  {i}. {pizza_dict['name']} ({pizza_dict['size']}) - {pizza_dict['price']:.2f} {pizza_dict['currency']}")
    
    print("\n✅ Démonstration terminée avec succès!")


if __name__ == "__main__":
    main()
