# 🍕 Pizza Delivery API

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)

**API REST Flask complète pour la gestion de livraison de pizzas**, développée avec l'approche **TDD (Test-Driven Development)**.

## ✨ Fonctionnalités Principales

- 🍕 **Gestion des pizzas** - Créer, consulter et gérer un menu de pizzas
- 📦 **Gestion des commandes** - Validation automatique (min 1 pizza)
- 🚗 **Suivi de livraison** - Tracking en temps réel
- 🎨 **Interface web moderne** - Design avec animations fluides

---

## 🚀 Démarrage Rapide

### Installation

```bash
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement (Windows CMD)
venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

### Lancer l'Application

```bash
# Démarrer le serveur Flask
python run.py
```

L'application sera accessible sur:
- 🌐 **Interface Web**: http://localhost:5000
- 🔌 **API REST**: http://localhost:5000/health

### Vérifier le Fonctionnement

```bash
# Test de santé de l'API
curl http://localhost:5000/health
```

Réponse attendue:
```json
{
    "status": "healthy",
    "message": "Pizza API is running"
}
```

---

## 🏗️ Architecture

### Classes Métier (avec TDD)

```
┌──────────────┐
│    Price     │  💰 Gestion multi-devises
│   (20 tests) │
└──────┬───────┘
       │
       ↓
┌──────────────┐      ┌──────────────┐
│    Pizza     │◄─────│    Order     │  📦 Validation automatique
│   (7 tests)  │      │  (15 tests)  │
└──────────────┘      └──────┬───────┘
                             │
                             ↓
                      ┌──────────────┐
                      │   Delivery   │  🚗 Tracking GPS
                      │  (11 tests)  │
                      └──────────────┘
```

### Stack Technique

- **Backend**: Flask 2.3+ (Python 3.9+)
- **Base de données**: SQLAlchemy + SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Tests**: pytest + pytest-cov
- **API**: REST JSON

---

## 📡 API Endpoints (19 endpoints)

### 🍕 Pizzas
| Méthode | Endpoint | Description | Statut |
|---------|----------|-------------|--------|
| `POST` | `/pizzas` | Créer une pizza | ✅ |
| `POST` | `/pizzas` | Créer une pizza (admin) | ✅ |
| `GET` | `/pizzas/<id>` | Récupérer une pizza | ✅ |
| `GET` | `/pizzas/catalog` | Récupérer le catalogue (groupé par nom) | ✅ NEW |

### 📦 Commandes

| Méthode | Endpoint | Description | Statut |
|---------|----------|-------------|-------|
| `POST` | `/orders` | Créer une commande | ✅ |
| `GET` | `/orders` | Lister les commandes | ✅ |
| `GET` | `/orders/<id>` | Récupérer une commande | ✅ |
| `POST` | `/orders/<id>/pizzas` | Ajouter une pizza | ✅ |
| `POST` | `/orders/<id>/pizzas` | Ajouter une pizza (par pizza_id) | ✅ |
| `PATCH` | `/orders/<id>/status` | Changer le statut | ✅ |

### 🚗 Livraisons

| Méthode | Endpoint | Description | Statut |
|---------|----------|-------------|--------|
| `POST` | `/deliveries` | Créer une livraison | ✅ |
| `GET` | `/deliveries/<id>` | Récupérer une livraison | ✅ |
| `PATCH` | `/deliveries/<id>/start` | Démarrer la livraison | ✅ |
| `PATCH` | `/deliveries/<id>/complete` | Terminer la livraison | ✅ |
| `PATCH` | `/deliveries/<id>/location` | Mettre à jour GPS | ✅ |
| `PATCH` | `/deliveries/<id>/cancel` | Annuler la livraison | ✅ |

### 🏥 Santé

| Méthode | Endpoint | Description | Statut |
|---------|----------|-------------|--------|
| `GET` | `/health` | Vérifier l'état de l'API | ✅ |

**📖 Documentation complète**: Voir [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🧪 Tests

### Lancer les Tests

```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=app tests/

# Tests verbeux
pytest -v

# Tests spécifiques
pytest tests/test_e2e.py -v
```
---

## 📂 Structure du Projet

```
pizza_api/
├── app/
│   ├── __init__.py
│   ├── app.py                 # Application Flask (19 endpoints)
│   ├── database.py            # Configuration SQLAlchemy
│   └── models/
│       ├── __init__.py
│       ├── pizza.py           # Modèle Pizza
│       ├── order.py           # Modèle Order (avec validation)
│       ├── delivery.py        # Modèle Delivery
│       ├── price.py           # Modèle Price (multi-devises)
│       └── db_models.py       # Modèles base de données
│
├── static/
│   ├── css/
│   │   └── style.css          # Styles UI moderne
│   └── js/
│       └── app.js             # Logique JavaScript
│
├── templates/
│   └── index.html             # Interface web
│
├── tests/
│   ├── __init__.py
│   ├── test_pizza.py          # Tests unitaires Pizza
│   ├── test_order.py          # Tests unitaires Order
│   ├── test_delivery.py       # Tests unitaires Delivery
│   ├── test_price.py          # Tests unitaires Price
│   └── test_e2e.py            # Tests end-to-end
│
├── run.py                     # Point d'entrée
├── requirements.txt           # Dépendances Python
├── README.md                  # Ce fichier
├── API_DOCUMENTATION.md       # Documentation API détaillée
└── pizza_delivery.db          # Base de données SQLite
```

---

## 🎯 Fonctionnalités

### Price
- ✅ Gestion multi-devises (EUR, USD, GBP, CAD)
- ✅ Opérations arithmétiques (addition, soustraction, multiplication)
- ✅ Comparaisons de prix
- ✅ Application de réductions et taxes
- ✅ Formatage avec ou sans symboles

### Pizza
- ✅ Création avec nom, taille, prix et garnitures
- ✅ Validation de taille (Small, Medium, Large)
- ✅ Validation de prix (non négatif)
- ✅ Support des prix avec devises (Price)
- ✅ Ajout/suppression de garnitures

### Order
- ✅ Création avec client et adresse
- ✅ **Validation : au moins une pizza obligatoire**
- ✅ Ajout/suppression de pizzas
- ✅ Calcul automatique du total (avec Price)
- ✅ Gestion des statuts (pending, preparing, ready, etc.)
- ✅ **Validation automatique lors du changement de statut**
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
