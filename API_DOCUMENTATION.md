# API Documentation - Pizza Delivery API

## Base URL
```
http://localhost:5000
```

## Endpoints

### 🏥 Health Check

#### GET /health
Vérifie que l'API est en ligne.

**Response 200:**
```json
{
  "status": "healthy",
  "message": "Pizza API is running"
}
```

---

## 🍕 Pizza Endpoints

### POST /pizzas
Crée une nouvelle pizza.

**Request Body:**
```json
{
  "name": "Margherita",
  "size": "Medium",
  "price": 12.99,
  "toppings": ["tomato", "mozzarella", "basil"]
}
```

**Response 201:**
```json
{
  "pizza_id": "1",
  "name": "Margherita",
  "size": "Medium",
  "price": 12.99,
  "toppings": ["tomato", "mozzarella", "basil"]
}
```

**Errors:**
- 400: Invalid data (invalid size or negative price)

---

### GET /pizzas/{pizza_id}
Récupère une pizza par son ID.

**Response 200:**
```json
{
  "pizza_id": "1",
  "name": "Margherita",
  "size": "Medium",
  "price": 12.99,
  "toppings": ["tomato", "mozzarella", "basil"]
}
```

**Errors:**
- 404: Pizza not found

---

### GET /pizzas
Récupère toutes les pizzas.

**Response 200:**
```json
{
  "pizzas": [
    {
      "pizza_id": "1",
      "name": "Margherita",
      "size": "Medium",
      "price": 12.99,
      "toppings": ["tomato", "mozzarella", "basil"]
    }
  ],
  "count": 1
}
```

---

## 📦 Order Endpoints

### POST /orders
Crée une nouvelle commande.

**Request Body:**
```json
{
  "customer_name": "John Doe",
  "customer_address": "123 Main St"
}
```

**Response 201:**
```json
{
  "order_id": "uuid-xxx",
  "customer_name": "John Doe",
  "customer_address": "123 Main St",
  "status": "pending",
  "pizzas": [],
  "total": 0,
  "created_at": "2025-10-27T10:00:00"
}
```

---

### GET /orders/{order_id}
Récupère une commande par son ID.

**Response 200:**
```json
{
  "order_id": "uuid-xxx",
  "customer_name": "John Doe",
  "customer_address": "123 Main St",
  "status": "pending",
  "pizzas": [],
  "total": 0,
  "created_at": "2025-10-27T10:00:00"
}
```

**Errors:**
- 404: Order not found

---

### GET /orders
Récupère toutes les commandes.

**Response 200:**
```json
{
  "orders": [...],
  "count": 5
}
```

---

### POST /orders/{order_id}/pizzas
Ajoute une pizza à une commande.

**Option 1 - Créer une nouvelle pizza:**
```json
{
  "name": "Pepperoni",
  "size": "Large",
  "price": 15.99,
  "toppings": ["pepperoni", "cheese"]
}
```

**Option 2 - Utiliser une pizza existante:**
```json
{
  "pizza_id": "1"
}
```

**Response 200:**
```json
{
  "order_id": "uuid-xxx",
  "customer_name": "John Doe",
  "customer_address": "123 Main St",
  "status": "pending",
  "pizzas": [
    {
      "name": "Pepperoni",
      "size": "Large",
      "price": 15.99,
      "toppings": ["pepperoni", "cheese"]
    }
  ],
  "total": 15.99,
  "created_at": "2025-10-27T10:00:00"
}
```

**Errors:**
- 404: Order not found or Pizza not found

---

### DELETE /orders/{order_id}/pizzas/{pizza_index}
Retire une pizza d'une commande.

**Response 200:**
```json
{
  "order_id": "uuid-xxx",
  "pizzas": [],
  "total": 0
}
```

**Errors:**
- 404: Order not found
- 400: Invalid pizza index

---

### PATCH /orders/{order_id}/status
Met à jour le statut d'une commande.

**Request Body:**
```json
{
  "status": "preparing"
}
```

**Valid statuses:**
- `pending`
- `preparing`
- `ready`
- `out_for_delivery`
- `delivered`
- `cancelled`

**Response 200:**
```json
{
  "order_id": "uuid-xxx",
  "status": "preparing",
  ...
}
```

**Errors:**
- 404: Order not found
- 400: Invalid status

---

## 🚚 Delivery Endpoints

### POST /deliveries
Crée une nouvelle livraison.

**Request Body:**
```json
{
  "order_id": "uuid-xxx",
  "driver_name": "Mike Driver"
}
```

**Response 201:**
```json
{
  "delivery_id": "uuid-yyy",
  "driver_name": "Mike Driver",
  "status": "assigned",
  "order": {...},
  "started_at": null,
  "completed_at": null,
  "current_latitude": null,
  "current_longitude": null,
  "cancellation_reason": null,
  "estimated_time": 30
}
```

**Errors:**
- 404: Order not found

---

### GET /deliveries/{delivery_id}
Récupère une livraison par son ID.

**Response 200:**
```json
{
  "delivery_id": "uuid-yyy",
  "driver_name": "Mike Driver",
  "status": "assigned",
  "order": {...},
  "started_at": null,
  "completed_at": null,
  "current_latitude": null,
  "current_longitude": null,
  "cancellation_reason": null,
  "estimated_time": 30
}
```

**Errors:**
- 404: Delivery not found

---

### GET /deliveries
Récupère toutes les livraisons.

**Response 200:**
```json
{
  "deliveries": [...],
  "count": 3
}
```

---

### PATCH /deliveries/{delivery_id}/start
Démarre une livraison.

**Response 200:**
```json
{
  "delivery_id": "uuid-yyy",
  "status": "in_transit",
  "started_at": "2025-10-27T10:15:00",
  ...
}
```

**Errors:**
- 404: Delivery not found
- 400: Delivery already started

---

### PATCH /deliveries/{delivery_id}/complete
Complète une livraison.

**Response 200:**
```json
{
  "delivery_id": "uuid-yyy",
  "status": "delivered",
  "started_at": "2025-10-27T10:15:00",
  "completed_at": "2025-10-27T10:45:00",
  ...
}
```

**Errors:**
- 404: Delivery not found
- 400: Delivery must be started before completion

---

### PATCH /deliveries/{delivery_id}/location
Met à jour la position GPS du livreur.

**Request Body:**
```json
{
  "latitude": 48.8566,
  "longitude": 2.3522
}
```

**Response 200:**
```json
{
  "delivery_id": "uuid-yyy",
  "current_latitude": 48.8566,
  "current_longitude": 2.3522,
  ...
}
```

**Errors:**
- 404: Delivery not found

---

### PATCH /deliveries/{delivery_id}/cancel
Annule une livraison.

**Request Body:**
```json
{
  "reason": "Customer not available"
}
```

**Response 200:**
```json
{
  "delivery_id": "uuid-yyy",
  "status": "cancelled",
  "cancellation_reason": "Customer not available",
  ...
}
```

**Errors:**
- 404: Delivery not found

---

## Error Responses

Toutes les erreurs suivent ce format:

```json
{
  "error": "Description of the error"
}
```

**Common HTTP Status Codes:**
- `200 OK` - Requête réussie
- `201 Created` - Ressource créée avec succès
- `400 Bad Request` - Données invalides
- `404 Not Found` - Ressource non trouvée
- `500 Internal Server Error` - Erreur serveur
