# Script pour lancer tous les tests
Write-Host "🧪 Lancement des tests unitaires..." -ForegroundColor Cyan
C:/Users/ALX/Projects/pizza_api/.venv/Scripts/python.exe -m pytest tests/test_pizza.py tests/test_order.py tests/test_delivery.py -v

Write-Host "`n🌐 Lancement des tests E2E..." -ForegroundColor Cyan
C:/Users/ALX/Projects/pizza_api/.venv/Scripts/python.exe -m pytest tests/test_e2e.py -v

Write-Host "`n📊 Rapport de couverture..." -ForegroundColor Cyan
C:/Users/ALX/Projects/pizza_api/.venv/Scripts/python.exe -m pytest --cov=app tests/ --cov-report=term-missing
