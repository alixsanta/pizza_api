# Guide de contribution 🤝

Merci de votre intérêt pour contribuer au projet Pizza Delivery API !

## 🚀 Configuration de l'environnement

1. **Fork et clone le projet**
```bash
git clone https://github.com/votre-username/pizza_api.git
cd pizza_api
```

2. **Créer un environnement virtuel**
```bash
python -m venv .venv
```

3. **Activer l'environnement**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Vérifier que tout fonctionne**
```bash
pytest
```

## 📝 Workflow de contribution

### 1. Créer une branche
```bash
git checkout -b feature/nom-de-la-feature
```

### 2. Développer en TDD

Ce projet suit l'approche **Test-Driven Development (TDD)** :

1. **RED** : Écrire les tests en premier (ils doivent échouer)
2. **GREEN** : Implémenter le code minimum pour faire passer les tests
3. **REFACTOR** : Améliorer le code sans casser les tests

**Exemple :**
```python
# 1. Écrire le test dans tests/test_nouvelle_feature.py
def test_nouvelle_fonctionnalite():
    result = ma_fonction()
    assert result == "attendu"

# 2. Lancer les tests (ils échouent) - RED
pytest tests/test_nouvelle_feature.py

# 3. Implémenter le code - GREEN
def ma_fonction():
    return "attendu"

# 4. Les tests passent !
pytest tests/test_nouvelle_feature.py

# 5. Refactoriser si nécessaire - REFACTOR
```

### 3. Tester votre code

Avant de commit, assurez-vous que :

```bash
# Tous les tests passent
pytest

# La couverture de code est bonne
pytest --cov=app tests/

# Les tests E2E passent
pytest tests/test_e2e.py -v

# Pas d'erreurs de linting (si configuré)
# flake8 app/
```

### 4. Commit vos changements

Utilisez des messages de commit clairs et descriptifs :

```bash
git add .
git commit -m "feat: ajouter la fonctionnalité X"
```

**Convention des messages de commit :**
- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `test:` ajout ou modification de tests
- `docs:` mise à jour de la documentation
- `refactor:` refactorisation du code
- `style:` formatage, indentation
- `chore:` tâches de maintenance

### 5. Push et créer une Pull Request

```bash
git push origin feature/nom-de-la-feature
```

Puis créez une Pull Request sur GitHub avec :
- Une description claire de ce qui a été fait
- Les tests ajoutés
- Des captures d'écran si pertinent

## 🧪 Standards de qualité

### Tests
- **Couverture** : Minimum 80% de couverture de code
- **Tests unitaires** : Pour chaque classe/fonction
- **Tests E2E** : Pour les nouveaux endpoints

### Code
- **PEP 8** : Suivre les conventions Python
- **Docstrings** : Documenter les fonctions et classes
- **Type hints** : Utiliser les annotations de type quand possible

### Documentation
- Mettre à jour `API_DOCUMENTATION.md` pour les nouveaux endpoints
- Mettre à jour le `README.md` si nécessaire
- Ajouter des exemples d'utilisation

## 📁 Structure du code

```
app/
├── models/           # Classes métier (Pizza, Order, Delivery)
├── app.py           # Application Flask et routes
└── __init__.py

tests/
├── test_pizza.py     # Tests unitaires Pizza
├── test_order.py     # Tests unitaires Order
├── test_delivery.py  # Tests unitaires Delivery
└── test_e2e.py      # Tests end-to-end
```

## 🐛 Signaler un bug

1. Vérifiez que le bug n'a pas déjà été signalé
2. Créez une issue avec :
   - Description claire du problème
   - Steps pour reproduire
   - Comportement attendu vs actuel
   - Version de Python utilisée

## 💡 Proposer une nouvelle fonctionnalité

1. Créez une issue pour discuter de la fonctionnalité
2. Attendez l'approbation avant de commencer le développement
3. Suivez le workflow TDD

## 🤔 Questions ?

N'hésitez pas à ouvrir une issue avec le label `question` !

## 📜 Code de conduite

- Soyez respectueux et professionnel
- Acceptez les critiques constructives
- Focalisez sur ce qui est le mieux pour le projet

Merci de contribuer ! 🍕
