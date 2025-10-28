# Exemples de requêtes curl pour tester l'API

## Health Check
curl http://localhost:5000/health

## PIZZAS

# Créer une pizza Margherita
curl -X POST http://localhost:5000/pizzas \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Margherita",
    "size": "Medium",
    "price": 12.99,
    "toppings": ["tomato", "mozzarella", "basil"]
  }'

# Créer une pizza Pepperoni
curl -X POST http://localhost:5000/pizzas \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pepperoni",
    "size": "Large",
    "price": 15.99,
    "toppings": ["pepperoni", "cheese"]
  }'

# Récupérer toutes les pizzas
curl http://localhost:5000/pizzas

# Récupérer une pizza par ID
curl http://localhost:5000/pizzas/1

## ORDERS

# Créer une commande
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_address": "123 Main St"
  }'

# Note: Sauvegarder le order_id retourné pour les commandes suivantes
# Par exemple: export ORDER_ID="uuid-xxx"

# Récupérer toutes les commandes
curl http://localhost:5000/orders

# Récupérer une commande par ID
curl http://localhost:5000/orders/$ORDER_ID

# Ajouter une pizza existante à la commande
curl -X POST http://localhost:5000/orders/$ORDER_ID/pizzas \
  -H "Content-Type: application/json" \
  -d '{
    "pizza_id": "1"
  }'

# Ou créer et ajouter une nouvelle pizza directement
curl -X POST http://localhost:5000/orders/$ORDER_ID/pizzas \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Supreme",
    "size": "Large",
    "price": 18.99,
    "toppings": ["pepperoni", "mushrooms", "olives"]
  }'

# Retirer une pizza de la commande (index 0)
curl -X DELETE http://localhost:5000/orders/$ORDER_ID/pizzas/0

# Mettre à jour le statut de la commande
curl -X PATCH http://localhost:5000/orders/$ORDER_ID/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "preparing"
  }'

# Autres statuts disponibles: "pending", "preparing", "ready", "out_for_delivery", "delivered", "cancelled"

## DELIVERIES

# Créer une livraison
curl -X POST http://localhost:5000/deliveries \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "'$ORDER_ID'",
    "driver_name": "Mike Driver"
  }'

# Note: Sauvegarder le delivery_id retourné
# Par exemple: export DELIVERY_ID="uuid-yyy"

# Récupérer toutes les livraisons
curl http://localhost:5000/deliveries

# Récupérer une livraison par ID
curl http://localhost:5000/deliveries/$DELIVERY_ID

# Démarrer la livraison
curl -X PATCH http://localhost:5000/deliveries/$DELIVERY_ID/start

# Mettre à jour la position GPS du livreur
curl -X PATCH http://localhost:5000/deliveries/$DELIVERY_ID/location \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 48.8566,
    "longitude": 2.3522
  }'

# Compléter la livraison
curl -X PATCH http://localhost:5000/deliveries/$DELIVERY_ID/complete

# Annuler une livraison
curl -X PATCH http://localhost:5000/deliveries/$DELIVERY_ID/cancel \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Customer not available"
  }'

## FLUX COMPLET E2E

# 1. Créer une pizza
PIZZA_RESPONSE=$(curl -s -X POST http://localhost:5000/pizzas \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hawaiian",
    "size": "Medium",
    "price": 14.99,
    "toppings": ["ham", "pineapple"]
  }')
echo "Pizza créée: $PIZZA_RESPONSE"

# 2. Créer une commande
ORDER_RESPONSE=$(curl -s -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Test Customer",
    "customer_address": "456 Oak Ave"
  }')
echo "Commande créée: $ORDER_RESPONSE"

# Extraire l'order_id (nécessite jq)
# ORDER_ID=$(echo $ORDER_RESPONSE | jq -r '.order_id')

# 3. Ajouter la pizza à la commande
# curl -X POST http://localhost:5000/orders/$ORDER_ID/pizzas \
#   -H "Content-Type: application/json" \
#   -d '{"pizza_id": "1"}'

# 4. Mettre à jour le statut
# curl -X PATCH http://localhost:5000/orders/$ORDER_ID/status \
#   -H "Content-Type: application/json" \
#   -d '{"status": "ready"}'

# 5. Créer une livraison
# curl -X POST http://localhost:5000/deliveries \
#   -H "Content-Type: application/json" \
#   -d '{
#     "order_id": "'$ORDER_ID'",
#     "driver_name": "Sarah Driver"
#   }'

# 6. Démarrer et compléter la livraison
# curl -X PATCH http://localhost:5000/deliveries/$DELIVERY_ID/start
# curl -X PATCH http://localhost:5000/deliveries/$DELIVERY_ID/complete
