# Guide de démarrage rapide - Pizza Delivery API 🍕

## Installation rapide

1. **Cloner et installer**
```powershell
cd c:\Users\ALX\Projects\pizza_api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. **Lancer l'API**
```powershell
python run.py
```

L'API sera disponible sur `http://localhost:5000`

## Tests rapides

### 1. Tests unitaires + E2E
```powershell
# Tous les tests
pytest

# Avec couverture
pytest --cov=app tests/

# Seulement les tests unitaires
pytest tests/test_pizza.py tests/test_order.py tests/test_delivery.py -v

# Seulement les tests E2E
pytest tests/test_e2e.py -v
```

### 2. Test manuel avec PowerShell
```powershell
# Lancer l'API dans un terminal
python run.py

# Dans un autre terminal, exécuter le script de test
.\test_api.ps1
```

### 3. Test avec VS Code Tasks
Appuyez sur `Ctrl+Shift+P` puis:
- "Tasks: Run Task" → "Run API Server" (lancer l'API)
- "Tasks: Run Task" → "Run All Tests" (tous les tests)
- "Tasks: Run Task" → "Run E2E Tests" (tests E2E)

## Architecture

```
3 Classes métier (TDD) → API REST Flask → Tests E2E
     ↓                        ↓               ↓
  Pizza.py              17 endpoints      test_e2e.py
  Order.py           (GET/POST/PATCH)    (14 scénarios)
  Delivery.py         JSON responses
```

## Endpoints principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/health` | Santé de l'API |
| POST | `/pizzas` | Créer une pizza |
| POST | `/orders` | Créer une commande |
| POST | `/orders/{id}/pizzas` | Ajouter pizza |
| PATCH | `/orders/{id}/status` | Changer statut |
| POST | `/deliveries` | Créer livraison |
| PATCH | `/deliveries/{id}/start` | Démarrer |
| PATCH | `/deliveries/{id}/complete` | Terminer |

Voir `API_DOCUMENTATION.md` pour la liste complète.

## Fichiers utiles

- `API_DOCUMENTATION.md` - Documentation complète de l'API
- `postman_collection.json` - Collection Postman
- `test_api.ps1` - Script de test PowerShell
- `curl_examples.sh` - Exemples curl

## Résultats des tests

✅ **27 tests unitaires** (Pizza, Order, Delivery)
✅ **14 tests E2E** (Flux complets)
✅ **1 test d'intégration complet** (Pizza → Order → Delivery)

## Prochaines étapes

1. Ajouter une base de données (SQLite/PostgreSQL)
2. Ajouter l'authentification JWT
3. Ajouter des webhooks pour les notifications
4. Déployer sur un serveur (Heroku, Railway, etc.)
