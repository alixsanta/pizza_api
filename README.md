# Pizza Delivery API

API Flask pour la gestion de livraison de pizzas.

## Installation

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Tests (TDD)

```bash
pytest
pytest --cov=app tests/
```

## Structure

- `app/models/` - Classes métier (Pizza, Order, Delivery)
- `tests/` - Tests unitaires
