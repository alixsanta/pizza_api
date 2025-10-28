# Pizza Delivery API 🍕

API REST Flask pour la gestion de livraison de pizzas, développée en TDD (Test-Driven Development).

## 🚀 Installation

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## 🏃 Lancer l'API

```bash
python run.py
```

L'API sera accessible sur `http://localhost:5000`

### Vérifier que l'API fonctionne

```bash
curl http://localhost:5000/health
```

## 🧪 Tests

### Tests unitaires (TDD)

```bash
# Tous les tests
pytest

# Tests avec couverture de code
pytest --cov=app tests/

# Tests verbeux
pytest -v
```

### Tests E2E

```bash
# Lancer d'abord l'API
python run.py

# Dans un autre terminal, lancer les tests E2E
pytest tests/test_e2e.py -v
```

## 📁 Structure du projet

```
pizza_api/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pizza.py       # Classe Pizza
│   │   ├── order.py       # Classe Order
│   │   └── delivery.py    # Classe Delivery
│   └── app.py             # Application Flask avec tous les endpoints
├── tests/
│   ├── test_pizza.py      # Tests unitaires Pizza
│   ├── test_order.py      # Tests unitaires Order
│   ├── test_delivery.py   # Tests unitaires Delivery
│   └── test_e2e.py        # Tests end-to-end
├── run.py                 # Point d'entrée de l'API
├── requirements.txt       # Dépendances Python
├── API_DOCUMENTATION.md   # Documentation complète de l'API
└── README.md             # Ce fichier
```

## 📚 Documentation de l'API

Voir [API_DOCUMENTATION.md](API_DOCUMENTATION.md) pour la documentation complète des endpoints.

### Endpoints principaux

- **Pizzas**: `POST /pizzas`, `GET /pizzas`, `GET /pizzas/{id}`
- **Commandes**: `POST /orders`, `GET /orders`, `GET /orders/{id}`, `PATCH /orders/{id}/status`
- **Livraisons**: `POST /deliveries`, `GET /deliveries`, `PATCH /deliveries/{id}/start`, `PATCH /deliveries/{id}/complete`

## 🏗️ Approche TDD

Ce projet a été développé en suivant l'approche Test-Driven Development :

1. ✅ **Phase RED** : Écriture des tests qui échouent
2. ✅ **Phase GREEN** : Implémentation du code pour faire passer les tests
3. ✅ **Phase REFACTOR** : Amélioration du code sans casser les tests

### Couverture des tests

- **27 tests unitaires** pour les 3 classes métier
- **Tests E2E** pour valider l'ensemble de l'API

## 🛠️ Technologies utilisées

- **Python 3.12**
- **Flask 3.0** - Framework web
- **pytest 7.4** - Framework de tests
- **pytest-cov** - Couverture de code

## 📝 Exemple d'utilisation

```bash
# 1. Créer une pizza
curl -X POST http://localhost:5000/pizzas \
  -H "Content-Type: application/json" \
  -d '{"name": "Margherita", "size": "Medium", "price": 12.99}'

# 2. Créer une commande
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "John Doe", "customer_address": "123 Main St"}'

# 3. Ajouter une pizza à la commande
curl -X POST http://localhost:5000/orders/{order_id}/pizzas \
  -H "Content-Type: application/json" \
  -d '{"pizza_id": "1"}'

# 4. Créer une livraison
curl -X POST http://localhost:5000/deliveries \
  -H "Content-Type: application/json" \
  -d '{"order_id": "{order_id}", "driver_name": "Mike Driver"}'

# 5. Démarrer la livraison
curl -X PATCH http://localhost:5000/deliveries/{delivery_id}/start

# 6. Compléter la livraison
curl -X PATCH http://localhost:5000/deliveries/{delivery_id}/complete
```

## 🎯 Fonctionnalités

### Pizza
- ✅ Création avec nom, taille, prix et garnitures
- ✅ Validation de taille (Small, Medium, Large)
- ✅ Validation de prix (non négatif)
- ✅ Ajout/suppression de garnitures

### Order
- ✅ Création avec client et adresse
- ✅ Ajout/suppression de pizzas
- ✅ Calcul automatique du total
- ✅ Gestion des statuts (pending, preparing, ready, etc.)
- ✅ Horodatage de création

### Delivery
- ✅ Création avec commande et livreur
- ✅ Démarrage et complétion de livraison
- ✅ Suivi GPS en temps réel
- ✅ Calcul de durée de livraison
- ✅ Annulation avec raison
- ✅ Temps estimé de livraison

## 🤝 Contribution

Ce projet a été développé dans un contexte d'apprentissage du TDD.
