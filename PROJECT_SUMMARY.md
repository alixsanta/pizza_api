# 🍕 Pizza Delivery API - Résumé du Projet

## 📊 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────┐
│         PIZZA DELIVERY API (Approche TDD)               │
│                                                          │
│  4 Classes Métier    →    17 Endpoints REST             │
│  57+ Tests           →    Documentation complète         │
└─────────────────────────────────────────────────────────┘
```

## 🏗️ Architecture

```
┌──────────────┐
│    Price     │  ← Nouvelle classe !
│ Multi-devises│
└──────┬───────┘
       │
       ↓
┌──────────────┐      ┌──────────────┐
│    Pizza     │◄─────│    Order     │  ← Validation !
│  (utilise    │      │ (min 1 pizza)│
│   Price)     │      └──────┬───────┘
└──────────────┘             │
                             ↓
                      ┌──────────────┐
                      │   Delivery   │
                      └──────────────┘
```

## ✨ Nouvelles fonctionnalités

### 1. Classe Price 💰
```python
# Support multi-devises
price = Price(amount=12.99, currency="EUR")

# Opérations
total = price1 + price2
discounted = price.apply_discount(10)  # -10%
with_tax = price.apply_tax(20)        # +20% TVA

# Formatage
print(price.format(with_symbol=True))  # "12.99 €"
```

**Tests : 20 tests unitaires**

### 2. Validation des commandes ✅
```python
# Une commande DOIT avoir au moins 1 pizza
order = Order(customer_name="John", customer_address="123 Main")

order.is_valid()  # False ❌

order.add_pizza(pizza)
order.is_valid()  # True ✅

# Validation automatique lors du changement de statut
order.update_status("preparing")  # OK si valide, sinon ValueError
```

**Tests : +8 nouveaux tests de validation**

### 3. Intégration Pizza + Price 🍕
```python
# Rétrocompatible : accepte float
pizza1 = Pizza(name="Margherita", size="Medium", price=12.99)

# Ou objet Price
pizza2 = Pizza(name="Pepperoni", size="Large", 
               price=Price(15.99, "EUR"))

# Accès au prix
pizza1.price.amount     # 12.99
pizza1.price.currency   # "EUR"
```

## 📈 Statistiques

### Tests
| Type | Nombre | Description |
|------|--------|-------------|
| Price | 20 | Tests complets de la classe Price |
| Pizza | 8 | Tests avec intégration Price |
| Order | 18 | Tests avec validation (8 nouveaux) |
| Delivery | 11 | Tests complets |
| E2E | 14+ | Tests de bout en bout |
| **TOTAL** | **71+** | **Couverture complète** |

### Code
| Fichier | Lignes | Description |
|---------|--------|-------------|
| price.py | ~200 | Classe Price complète |
| pizza.py | ~70 | Avec support Price |
| order.py | ~120 | Avec validation |
| delivery.py | ~125 | Gestion livraisons |
| app.py | ~400 | 17 endpoints REST |
| **Tests** | **~1500** | **Tests complets** |

## 🎯 Fonctionnalités clés

### Price
- ✅ 4 devises supportées (EUR, USD, GBP, CAD)
- ✅ Addition, soustraction, multiplication
- ✅ Comparaisons (<, >, ==)
- ✅ Réductions et taxes
- ✅ Formatage avec symboles
- ✅ Validation stricte

### Order (avec validation)
- ✅ **Minimum 1 pizza obligatoire**
- ✅ **Validation auto lors du changement de statut**
- ✅ Calcul total avec Price
- ✅ Vérification des devises cohérentes
- ✅ Méthodes `is_valid()` et `validate()`

### Pizza (avec Price)
- ✅ Support Price object
- ✅ Rétrocompatibilité float
- ✅ Multi-devises
- ✅ Sérialisation JSON correcte

### Delivery
- ✅ Suivi GPS
- ✅ Calcul de durée
- ✅ États multiples
- ✅ Annulation avec raison

## 📚 Documentation

| Fichier | Description |
|---------|-------------|
| README.md | Documentation principale |
| API_DOCUMENTATION.md | 17 endpoints détaillés |
| PRICE_DOCUMENTATION.md | Guide complet Price |
| QUICKSTART.md | Démarrage rapide |
| BEFORE_PUSH.md | Checklist avant Git |
| CHANGELOG_PRICE.md | Nouveautés Price |

## 🧪 Approche TDD

```
1. RED    → Tests écrits (échouent)
2. GREEN  → Code implémenté (tests passent)
3. REFACTOR → Code amélioré
```

### Exemple pour Price
```
1. ✅ Écrire 20 tests pour Price
2. ✅ Implémenter Price pour faire passer les tests
3. ✅ Intégrer dans Pizza et Order
4. ✅ Ajouter tests de validation Order
```

## 🚀 Utilisation

### Démarrage rapide
```bash
# Installation
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Tests
pytest -v

# Exemple
python example_usage.py

# API
python run.py
```

### Exemple complet
```python
from app.models import Price, Pizza, Order, Delivery

# 1. Créer des pizzas avec prix
pizza1 = Pizza("Margherita", "Medium", 12.99)
pizza2 = Pizza("Pepperoni", "Large", Price(15.99, "EUR"))

# 2. Créer une commande
order = Order("John Doe", "123 Main St")
order.add_pizza(pizza1)
order.add_pizza(pizza2)

# 3. Vérifier et valider
assert order.is_valid()  # True ✅
order.validate()  # OK

# 4. Calculer le total
total = order.calculate_total()  # Price(28.98, EUR)
print(total.format(with_symbol=True))  # "28.98 €"

# 5. Appliquer réduction
discounted = total.apply_discount(10)  # "26.08 €"

# 6. Changer de statut
order.update_status("preparing")  # OK ✅

# 7. Créer livraison
delivery = Delivery(order, "Mike Driver")
delivery.start_delivery()
delivery.complete_delivery()
```

## 📦 Prêt pour Git

### ✅ À push
- Code source (app/)
- Tests (tests/)
- Documentation (*.md)
- Configuration (requirements.txt, setup.cfg)
- Outils (.vscode/tasks.json, postman_collection.json)

### ❌ Ignoré (.gitignore)
- .venv/ (environnement virtuel)
- __pycache__/ (cache Python)
- .pytest_cache/ (cache tests)
- .coverage, htmlcov/ (rapports)
- *.log (logs)
- .env (secrets)

## 🎉 Résultat final

✅ API REST complète avec 17 endpoints
✅ 4 classes métier avec TDD
✅ 71+ tests (couverture complète)
✅ Validation robuste des commandes
✅ Support multi-devises avec Price
✅ Documentation exhaustive
✅ Exemples et outils de test
✅ Prêt pour collaboration (Git)

**Temps de développement estimé : ~3-4 heures**
**Lignes de code : ~2500+ lignes (code + tests)**
**Approche : 100% TDD**

---

## 🌟 Points forts du projet

1. **Approche TDD rigoureuse** - Tests écrits avant le code
2. **Validation métier** - Règles strictes (min 1 pizza)
3. **Architecture propre** - Séparation des responsabilités
4. **Documentation complète** - README, API, guides
5. **Prêt pour production** - Tests, validation, multi-devises
6. **Facilement extensible** - Architecture modulaire
7. **Outils de test** - Scripts PowerShell, Postman, curl

**🍕 Projet prêt à être partagé avec vos collaborateurs ! 🚀**
