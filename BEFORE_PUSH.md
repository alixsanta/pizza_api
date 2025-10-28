# Checklist avant de push sur Git 📋

## ✅ Fichiers à NE PAS push (déjà dans .gitignore)

- `__pycache__/` - Cache Python
- `.venv/` ou `venv/` - Environnement virtuel
- `.pytest_cache/` - Cache des tests
- `.coverage` et `htmlcov/` - Rapports de couverture
- `*.log` - Fichiers de logs
- `.env` - Variables d'environnement
- `.DS_Store` - Fichiers macOS
- `*.db`, `*.sqlite` - Bases de données locales
- `.idea/`, `.vscode/` (sauf tasks.json) - Configuration IDE

## ✅ Fichiers à push (code source)

### Code principal
- ✅ `app/` - Tout le dossier application
  - `app/models/price.py`
  - `app/models/pizza.py`
  - `app/models/order.py`
  - `app/models/delivery.py`
  - `app/app.py`
- ✅ `tests/` - Tous les tests
  - `tests/test_price.py`
  - `tests/test_pizza.py`
  - `tests/test_order.py`
  - `tests/test_delivery.py`
  - `tests/test_e2e.py`

### Configuration
- ✅ `requirements.txt` - Dépendances
- ✅ `setup.cfg` - Configuration pytest
- ✅ `.gitignore` - Fichiers à ignorer
- ✅ `run.py` - Point d'entrée

### Documentation
- ✅ `README.md` - Documentation principale
- ✅ `API_DOCUMENTATION.md` - Documentation API
- ✅ `PRICE_DOCUMENTATION.md` - Documentation Price
- ✅ `QUICKSTART.md` - Guide rapide
- ✅ `CHANGELOG_PRICE.md` - Historique des changements

### Outils
- ✅ `.vscode/tasks.json` - Tasks VS Code
- ✅ `postman_collection.json` - Collection Postman
- ✅ `curl_examples.sh` - Exemples curl
- ✅ `test_api.ps1` - Script de test PowerShell
- ✅ `example_usage.py` - Exemple d'utilisation

## 🔍 Vérifications avant push

### 1. Vérifier qu'aucun fichier sensible n'est commité
```bash
git status
```

### 2. Vérifier les fichiers ignorés
```bash
git status --ignored
```

### 3. Tester que tout fonctionne
```bash
# Tests unitaires
pytest tests/test_price.py tests/test_pizza.py tests/test_order.py -v

# Exemple
python example_usage.py

# Tous les tests
pytest -v
```

### 4. Vérifier qu'il n'y a pas de .env ou secrets
```bash
# Chercher les fichiers .env
ls -la | grep .env

# Vérifier qu'aucun secret n'est dans le code
grep -r "password" app/
grep -r "secret" app/
grep -r "api_key" app/
```

## 📦 Commandes Git recommandées

### Initialiser (si pas déjà fait)
```bash
git init
git add .gitignore
git commit -m "Initial commit: Add .gitignore"
```

### Premier push
```bash
# Ajouter tous les fichiers (sauf ceux dans .gitignore)
git add .

# Vérifier ce qui va être commité
git status

# Commit
git commit -m "feat: Add Pizza Delivery API with Price class and validation

- Add Price class for multi-currency support
- Add validation: Order must have at least one pizza
- Add 57+ unit tests
- Add E2E tests
- Add comprehensive documentation"

# Push (remplacer par votre remote)
git remote add origin https://github.com/votre-username/pizza-api.git
git branch -M main
git push -u origin main
```

## 🤝 Pour les collaborateurs

### Fichiers à ignorer lors du clone
Assurez-vous que le `.gitignore` est bien respecté :
- Ne jamais commiter l'environnement virtuel
- Ne jamais commiter les fichiers `.env`
- Ne jamais commiter les bases de données locales

### Configuration initiale pour un collaborateur
```bash
# Clone
git clone https://github.com/votre-username/pizza-api.git
cd pizza-api

# Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Tester
pytest -v

# Lancer l'API
python run.py
```

## ⚠️ Attention

### Ne JAMAIS push :
- ❌ Mots de passe
- ❌ Clés API
- ❌ Tokens d'authentification
- ❌ Fichiers de configuration locaux avec des secrets
- ❌ Bases de données avec des données réelles
- ❌ Environnements virtuels
- ❌ Fichiers de cache

### Toujours push :
- ✅ Code source
- ✅ Tests
- ✅ Documentation
- ✅ requirements.txt
- ✅ .gitignore
- ✅ Configuration générique (sans secrets)

## 🎉 Checklist finale

Avant de push, vérifiez :

- [ ] Le `.gitignore` est en place
- [ ] Aucun fichier sensible dans `git status`
- [ ] Tous les tests passent : `pytest -v`
- [ ] L'exemple fonctionne : `python example_usage.py`
- [ ] La documentation est à jour
- [ ] Les `requirements.txt` sont corrects
- [ ] Le README est complet
- [ ] Les commit messages sont clairs

## 📝 Message de commit suggéré

```
feat: Pizza Delivery API with Price validation

Added features:
- Price class for multi-currency management (EUR, USD, GBP, CAD)
- Order validation: minimum 1 pizza required
- Pizza integration with Price object
- 57+ comprehensive unit tests
- E2E tests for complete workflow
- Full API documentation

TDD approach maintained throughout development.
```

Vous êtes prêt à push ! 🚀
