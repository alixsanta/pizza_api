# Classe Price - Documentation

## Description

La classe `Price` représente un prix avec un montant et une devise. Elle permet de :
- Gérer des prix dans différentes devises (EUR, USD, GBP, CAD)
- Effectuer des opérations arithmétiques (addition, soustraction, multiplication)
- Appliquer des réductions et des taxes
- Comparer des prix
- Formater des prix pour l'affichage

## Utilisation

### Création d'un prix

```python
from app.models import Price

# Prix en EUR (devise par défaut)
price1 = Price(amount=12.99)

# Prix en USD
price2 = Price(amount=19.99, currency="USD")
```

### Opérations arithmétiques

```python
# Addition
price1 = Price(amount=10.99, currency="EUR")
price2 = Price(amount=5.50, currency="EUR")
total = price1 + price2  # Price(16.49, EUR)

# Multiplication
price = Price(amount=10.00, currency="EUR")
total = price * 3  # Price(30.00, EUR)

# Soustraction
price1 = Price(amount=20.00, currency="EUR")
price2 = Price(amount=7.50, currency="EUR")
result = price1 - price2  # Price(12.50, EUR)
```

### Comparaisons

```python
price1 = Price(amount=20.00, currency="EUR")
price2 = Price(amount=10.00, currency="EUR")

price1 > price2  # True
price1 == price2  # False
price1 < price2  # False
```

### Réductions et taxes

```python
price = Price(amount=100.00, currency="EUR")

# Appliquer 20% de réduction
discounted = price.apply_discount(20)  # Price(80.00, EUR)

# Appliquer 20% de taxe (TVA)
with_tax = price.apply_tax(20)  # Price(120.00, EUR)
```

### Formatage

```python
price = Price(amount=12.99, currency="EUR")

# Format standard
str(price)  # "12.99 EUR"
price.format()  # "12.99 EUR"

# Format avec symbole
price.format(with_symbol=True)  # "12.99 €"

# USD avec symbole
price_usd = Price(amount=19.99, currency="USD")
price_usd.format(with_symbol=True)  # "$19.99"
```

### Conversion

```python
# Vers dictionnaire
price = Price(amount=25.50, currency="EUR")
price_dict = price.to_dict()  # {"amount": 25.50, "currency": "EUR"}

# Depuis dictionnaire
price_data = {"amount": 18.99, "currency": "USD"}
price = Price.from_dict(price_data)
```

## Intégration avec Pizza et Order

### Pizza avec Price

```python
from app.models import Pizza, Price

# Créer une pizza avec un float (automatiquement converti en Price)
pizza1 = Pizza(name="Margherita", size="Medium", price=12.99)

# Créer une pizza avec un objet Price
price = Price(amount=15.99, currency="EUR")
pizza2 = Pizza(name="Pepperoni", size="Large", price=price)

# Accéder au prix
pizza1.price  # Price(12.99, EUR)
pizza1.price.amount  # 12.99
pizza1.price.currency  # "EUR"
```

### Order avec validation

```python
from app.models import Order, Pizza

# Créer une commande
order = Order(customer_name="John Doe", customer_address="123 Main St")

# Vérifier si valide (False car pas de pizza)
order.is_valid()  # False

# Ajouter une pizza
pizza = Pizza(name="Supreme", size="Large", price=18.99)
order.add_pizza(pizza)

# Maintenant valide
order.is_valid()  # True

# Calculer le total (retourne un Price)
total = order.calculate_total()  # Price(18.99, EUR)
total.amount  # 18.99
total.currency  # "EUR"

# Valider avant de changer de statut
order.validate()  # OK, ne lève pas d'exception

# Changer de statut (nécessite au moins une pizza pour preparing, ready, etc.)
order.update_status("preparing")  # OK

# Tenter de changer sans pizza
empty_order = Order(customer_name="Jane", customer_address="456 Oak")
empty_order.update_status("preparing")  # ValueError: Order must have at least one pizza
```

## Validation des commandes

Une commande est considérée comme **valide** si elle contient **au moins une pizza**.

### Statuts nécessitant une validation

Les statuts suivants nécessitent une commande valide :
- `preparing`
- `ready`
- `out_for_delivery`
- `delivered`

Les statuts suivants n'ont pas besoin de validation :
- `pending` (état initial)
- `cancelled`

### Exemple de workflow

```python
from app.models import Order, Pizza

# 1. Créer une commande (statut: pending)
order = Order(customer_name="Alice", customer_address="789 Elm St")
print(order.status)  # "pending"
print(order.is_valid())  # False

# 2. Ajouter des pizzas
pizza1 = Pizza(name="Margherita", size="Medium", price=12.99)
pizza2 = Pizza(name="Pepperoni", size="Large", price=15.99)
order.add_pizza(pizza1)
order.add_pizza(pizza2)
print(order.is_valid())  # True

# 3. Calculer le total
total = order.calculate_total()
print(f"Total: {total.format(with_symbol=True)}")  # "Total: 28.98 €"

# 4. Passer en préparation (nécessite une validation)
order.update_status("preparing")  # OK

# 5. Marquer comme prêt
order.update_status("ready")  # OK

# 6. Créer une livraison...
```

## Devises supportées

| Code | Nom | Symbole |
|------|-----|---------|
| EUR | Euro | € |
| USD | Dollar US | $ |
| GBP | Livre Sterling | £ |
| CAD | Dollar Canadien | C$ |

## Règles de validation

1. **Montant négatif** : Interdit (ValueError)
2. **Devise invalide** : Interdit (ValueError)
3. **Opérations entre devises différentes** : Interdit (ValueError)
4. **Montant à 0** : Autorisé
5. **Arrondi** : Automatique à 2 décimales

## Exemples d'erreurs

```python
# Montant négatif
Price(amount=-10.00)  # ValueError: Price amount cannot be negative

# Devise invalide
Price(amount=10.00, currency="XXX")  # ValueError: Invalid currency

# Addition de devises différentes
price_eur = Price(amount=10.00, currency="EUR")
price_usd = Price(amount=10.00, currency="USD")
total = price_eur + price_usd  # ValueError: Cannot add prices with different currencies
```
