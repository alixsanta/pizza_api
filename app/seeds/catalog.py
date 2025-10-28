"""
Module de peuplement de la base de données
Contient toutes les données de démonstration pour le catalogue
"""
import json

# Données du catalogue de pizzas
CATALOG_PIZZAS = [
    # Pizzas Small
    {
        'name': 'Margherita',
        'size': 'Small',
        'price_amount': 8.99,
        'price_currency': 'EUR',
        'toppings': ['Tomato Sauce', 'Mozzarella', 'Basil']
    },
    {
        'name': 'Pepperoni',
        'size': 'Small',
        'price_amount': 9.99,
        'price_currency': 'EUR',
        'toppings': ['Tomato Sauce', 'Mozzarella', 'Pepperoni']
    },
    {
        'name': 'Vegetariana',
        'size': 'Small',
        'price_amount': 9.49,
        'price_currency': 'EUR',
        'toppings': ['Tomato Sauce', 'Mozzarella', 'Bell Peppers', 'Mushrooms', 'Onions', 'Olives']
    },

    # Pizzas Medium
    {
        'name': 'Margherita',
        'size': 'Medium',
        'price_amount': 11.99,
        'price_currency': 'EUR',
        'toppings': ['Tomato Sauce', 'Mozzarella', 'Basil']
    },
    {
        'name': 'Pepperoni',
        'size': 'Medium',
        'price_amount': 12.99,
        'price_currency': 'EUR',
        'toppings': ['Tomato Sauce', 'Mozzarella', 'Pepperoni']
    },
    {
        'name': 'Quattro Formaggi',
        'size': 'Medium',
        'price_amount': 13.99,
        'price_currency': 'EUR',
        'toppings': ['Mozzarella', 'Gorgonzola', 'Parmesan', 'Fontina']
    },
    {
        'name': 'Hawaienne',
        'size': 'Medium',
        'price_amount': 12.49,
        'price_currency': 'EUR',
        'toppings': ['Tomato Sauce', 'Mozzarella', 'Ham', 'Pineapple']
    },

    # Pizzas Large
    {
        'name': 'Margherita',
        'size': 'Large',
        'price_amount': 14.99,
        'price_currency': 'EUR',
        'toppings': ['Tomato Sauce', 'Mozzarella', 'Basil']
    },
    {
        'name': 'Pepperoni',
        'size': 'Large',
        'price_amount': 15.99,
        'price_currency': 'EUR',
        'toppings': ['Tomato Sauce', 'Mozzarella', 'Pepperoni']
    },
    {
        'name': 'Supreme',
        'size': 'Large',
        'price_amount': 17.99,
        'price_currency': 'EUR',
        'toppings': ['Tomato Sauce', 'Mozzarella', 'Pepperoni', 'Sausage', 'Bell Peppers', 'Onions', 'Mushrooms', 'Olives']
    },
    {
        'name': 'Diavola',
        'size': 'Large',
        'price_amount': 16.49,
        'price_currency': 'EUR',
        'toppings': ['Tomato Sauce', 'Mozzarella', 'Spicy Salami', 'Hot Peppers', 'Chili Flakes']
    },
    {
        'name': 'Calzone',
        'size': 'Large',
        'price_amount': 15.99,
        'price_currency': 'EUR',
        'toppings': ['Tomato Sauce', 'Mozzarella', 'Ham', 'Mushrooms', 'Ricotta']
    }
]

# Données d'exemples de commandes
SAMPLE_ORDERS = [
    {
        'customer_name': 'Jean Dupont',
        'customer_address': '123 Rue de la Pizza, 75001 Paris',
        'status': 'delivered',
        'pizzas_indices': [0, 1],  # Margherita Small, Pepperoni Small
        'delivery': {
            'driver_name': 'Jean Livreur',
            'status': 'delivered',
            'days_ago': 2
        }
    },
    {
        'customer_name': 'Marie Martin',
        'customer_address': '45 Avenue des Gourmets, 69002 Lyon',
        'status': 'in_delivery',
        'pizzas_indices': [2],  # Vegetariana Small
        'delivery': {
            'driver_name': 'Pierre Transport',
            'status': 'in_transit',
            'hours_ago': 1
        }
    },
    {
        'customer_name': 'Pierre Bernard',
        'customer_address': '78 Boulevard du Fromage, 13001 Marseille',
        'status': 'preparing',
        'pizzas_indices': [3, 5, 7],  # Margherita Medium, Quattro Formaggi, Margherita Large
        'delivery': {
            'driver_name': 'Luc Rapide',
            'status': 'assigned',
            'minutes_ago': 30
        }
    },
    {
        'customer_name': 'Sophie Laurent',
        'customer_address': '12 Place de la République, 33000 Bordeaux',
        'status': 'pending',
        'pizzas_indices': [4, 8],  # Pepperoni Medium, Pepperoni Large
        'delivery': None  # Pas encore de livraison
    }
]

