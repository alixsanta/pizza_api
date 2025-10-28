# Script PowerShell pour tester l'API Pizza Delivery

$baseUrl = "http://localhost:5000"

Write-Host "🍕 Test de l'API Pizza Delivery" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Health Check
Write-Host "1️⃣  Health Check..." -ForegroundColor Cyan
$health = Invoke-RestMethod -Uri "$baseUrl/health" -Method Get
Write-Host "   Status: $($health.status)" -ForegroundColor Yellow
Write-Host ""

# Créer une pizza
Write-Host "2️⃣  Création d'une pizza Margherita..." -ForegroundColor Cyan
$pizzaData = @{
    name = "Margherita"
    size = "Medium"
    price = 12.99
    toppings = @("tomato", "mozzarella", "basil")
} | ConvertTo-Json

$pizza = Invoke-RestMethod -Uri "$baseUrl/pizzas" -Method Post -Body $pizzaData -ContentType "application/json"
$pizzaId = $pizza.pizza_id
Write-Host "   Pizza créée avec ID: $pizzaId" -ForegroundColor Yellow
Write-Host ""

# Créer une commande
Write-Host "3️⃣  Création d'une commande..." -ForegroundColor Cyan
$orderData = @{
    customer_name = "John Doe"
    customer_address = "123 Main St"
} | ConvertTo-Json

$order = Invoke-RestMethod -Uri "$baseUrl/orders" -Method Post -Body $orderData -ContentType "application/json"
$orderId = $order.order_id
Write-Host "   Commande créée avec ID: $orderId" -ForegroundColor Yellow
Write-Host "   Client: $($order.customer_name)" -ForegroundColor Yellow
Write-Host ""

# Ajouter la pizza à la commande
Write-Host "4️⃣  Ajout de la pizza à la commande..." -ForegroundColor Cyan
$addPizzaData = @{
    pizza_id = $pizzaId
} | ConvertTo-Json

$updatedOrder = Invoke-RestMethod -Uri "$baseUrl/orders/$orderId/pizzas" -Method Post -Body $addPizzaData -ContentType "application/json"
Write-Host "   Nombre de pizzas: $($updatedOrder.pizzas.Count)" -ForegroundColor Yellow
Write-Host "   Total: $($updatedOrder.total) €" -ForegroundColor Yellow
Write-Host ""

# Mettre à jour le statut de la commande
Write-Host "5️⃣  Mise à jour du statut: preparing..." -ForegroundColor Cyan
$statusData = @{
    status = "preparing"
} | ConvertTo-Json

$updatedOrder = Invoke-RestMethod -Uri "$baseUrl/orders/$orderId/status" -Method Patch -Body $statusData -ContentType "application/json"
Write-Host "   Nouveau statut: $($updatedOrder.status)" -ForegroundColor Yellow
Write-Host ""

# Créer une livraison
Write-Host "6️⃣  Création d'une livraison..." -ForegroundColor Cyan
$deliveryData = @{
    order_id = $orderId
    driver_name = "Mike Driver"
} | ConvertTo-Json

$delivery = Invoke-RestMethod -Uri "$baseUrl/deliveries" -Method Post -Body $deliveryData -ContentType "application/json"
$deliveryId = $delivery.delivery_id
Write-Host "   Livraison créée avec ID: $deliveryId" -ForegroundColor Yellow
Write-Host "   Livreur: $($delivery.driver_name)" -ForegroundColor Yellow
Write-Host "   Statut: $($delivery.status)" -ForegroundColor Yellow
Write-Host ""

# Démarrer la livraison
Write-Host "7️⃣  Démarrage de la livraison..." -ForegroundColor Cyan
$startedDelivery = Invoke-RestMethod -Uri "$baseUrl/deliveries/$deliveryId/start" -Method Patch
Write-Host "   Statut: $($startedDelivery.status)" -ForegroundColor Yellow
Write-Host "   Démarrée à: $($startedDelivery.started_at)" -ForegroundColor Yellow
Write-Host ""

# Mettre à jour la position GPS
Write-Host "8️⃣  Mise à jour de la position GPS..." -ForegroundColor Cyan
$locationData = @{
    latitude = 48.8566
    longitude = 2.3522
} | ConvertTo-Json

$deliveryWithLocation = Invoke-RestMethod -Uri "$baseUrl/deliveries/$deliveryId/location" -Method Patch -Body $locationData -ContentType "application/json"
Write-Host "   Position: $($deliveryWithLocation.current_latitude), $($deliveryWithLocation.current_longitude)" -ForegroundColor Yellow
Write-Host ""

# Compléter la livraison
Write-Host "9️⃣  Complétion de la livraison..." -ForegroundColor Cyan
$completedDelivery = Invoke-RestMethod -Uri "$baseUrl/deliveries/$deliveryId/complete" -Method Patch
Write-Host "   Statut: $($completedDelivery.status)" -ForegroundColor Yellow
Write-Host "   Complétée à: $($completedDelivery.completed_at)" -ForegroundColor Yellow
Write-Host ""

# Récapitulatif
Write-Host "✅ FLUX COMPLET TERMINÉ AVEC SUCCÈS!" -ForegroundColor Green
Write-Host ""
Write-Host "Récapitulatif:" -ForegroundColor Cyan
Write-Host "  - Pizza ID: $pizzaId" -ForegroundColor White
Write-Host "  - Order ID: $orderId" -ForegroundColor White
Write-Host "  - Delivery ID: $deliveryId" -ForegroundColor White
Write-Host "  - Total commande: $($updatedOrder.total) €" -ForegroundColor White
Write-Host ""

# Récupérer les statistiques
Write-Host "📊 Statistiques:" -ForegroundColor Cyan
$allPizzas = Invoke-RestMethod -Uri "$baseUrl/pizzas" -Method Get
$allOrders = Invoke-RestMethod -Uri "$baseUrl/orders" -Method Get
$allDeliveries = Invoke-RestMethod -Uri "$baseUrl/deliveries" -Method Get

Write-Host "  - Pizzas créées: $($allPizzas.count)" -ForegroundColor White
Write-Host "  - Commandes créées: $($allOrders.count)" -ForegroundColor White
Write-Host "  - Livraisons créées: $($allDeliveries.count)" -ForegroundColor White
Write-Host ""
