import pytest
import json
from app.app import app


@pytest.fixture
def client():
    """Fixture pour le client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def reset_stores():
    """Fixture pour réinitialiser les stores entre les tests"""
    from app.app import pizzas_store, orders_store, deliveries_store
    pizzas_store.clear()
    orders_store.clear()
    deliveries_store.clear()
    yield
    pizzas_store.clear()
    orders_store.clear()
    deliveries_store.clear()


class TestHealthEndpoint:
    """Tests pour l'endpoint de santé"""
    
    def test_health_check(self, client):
        """Test que l'API répond au health check"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'


class TestPizzaEndpoints:
    """Tests E2E pour les endpoints Pizza"""
    
    def test_create_pizza(self, client, reset_stores):
        """Test la création d'une pizza via l'API"""
        pizza_data = {
            "name": "Margherita",
            "size": "Medium",
            "price": 12.99,
            "toppings": ["tomato", "mozzarella", "basil"]
        }
        
        response = client.post('/pizzas',
                               data=json.dumps(pizza_data),
                               content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == "Margherita"
        assert data['size'] == "Medium"
        assert data['price'] == 12.99
        assert 'pizza_id' in data
    
    def test_create_pizza_invalid_size(self, client, reset_stores):
        """Test qu'une taille invalide retourne une erreur"""
        pizza_data = {
            "name": "Test",
            "size": "Huge",
            "price": 10.99
        }
        
        response = client.post('/pizzas',
                               data=json.dumps(pizza_data),
                               content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_pizza(self, client, reset_stores):
        """Test la récupération d'une pizza"""
        # Créer une pizza d'abord
        pizza_data = {
            "name": "Pepperoni",
            "size": "Large",
            "price": 15.99
        }
        
        create_response = client.post('/pizzas',
                                      data=json.dumps(pizza_data),
                                      content_type='application/json')
        pizza_id = json.loads(create_response.data)['pizza_id']
        
        # Récupérer la pizza
        response = client.get(f'/pizzas/{pizza_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == "Pepperoni"
    
    def test_get_all_pizzas(self, client, reset_stores):
        """Test la récupération de toutes les pizzas"""
        # Créer plusieurs pizzas
        pizzas = [
            {"name": "Margherita", "size": "Small", "price": 10.99},
            {"name": "Pepperoni", "size": "Medium", "price": 12.99},
            {"name": "Supreme", "size": "Large", "price": 18.99}
        ]
        
        for pizza in pizzas:
            client.post('/pizzas',
                       data=json.dumps(pizza),
                       content_type='application/json')
        
        response = client.get('/pizzas')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 3
        assert len(data['pizzas']) == 3


class TestOrderEndpoints:
    """Tests E2E pour les endpoints Order"""
    
    def test_create_order(self, client, reset_stores):
        """Test la création d'une commande via l'API"""
        order_data = {
            "customer_name": "John Doe",
            "customer_address": "123 Main St"
        }
        
        response = client.post('/orders',
                              data=json.dumps(order_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['customer_name'] == "John Doe"
        assert data['customer_address'] == "123 Main St"
        assert data['status'] == "pending"
        assert 'order_id' in data
    
    def test_get_order(self, client, reset_stores):
        """Test la récupération d'une commande"""
        order_data = {
            "customer_name": "Jane Smith",
            "customer_address": "456 Oak Ave"
        }
        
        create_response = client.post('/orders',
                                      data=json.dumps(order_data),
                                      content_type='application/json')
        order_id = json.loads(create_response.data)['order_id']
        
        response = client.get(f'/orders/{order_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['customer_name'] == "Jane Smith"
    
    def test_add_pizza_to_order(self, client, reset_stores):
        """Test l'ajout d'une pizza à une commande"""
        # Créer une commande
        order_data = {
            "customer_name": "Bob Johnson",
            "customer_address": "789 Elm St"
        }
        order_response = client.post('/orders',
                                     data=json.dumps(order_data),
                                     content_type='application/json')
        order_id = json.loads(order_response.data)['order_id']
        
        # Ajouter une pizza
        pizza_data = {
            "name": "Margherita",
            "size": "Medium",
            "price": 12.99
        }
        response = client.post(f'/orders/{order_id}/pizzas',
                              data=json.dumps(pizza_data),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['pizzas']) == 1
        assert data['total'] == 12.99
    
    def test_update_order_status(self, client, reset_stores):
        """Test la mise à jour du statut d'une commande"""
        # Créer une commande
        order_data = {
            "customer_name": "Alice Brown",
            "customer_address": "321 Pine Rd"
        }
        order_response = client.post('/orders',
                                     data=json.dumps(order_data),
                                     content_type='application/json')
        order_id = json.loads(order_response.data)['order_id']
        
        # Mettre à jour le statut
        status_data = {"status": "preparing"}
        response = client.patch(f'/orders/{order_id}/status',
                               data=json.dumps(status_data),
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == "preparing"


class TestDeliveryEndpoints:
    """Tests E2E pour les endpoints Delivery"""
    
    def test_create_delivery(self, client, reset_stores):
        """Test la création d'une livraison via l'API"""
        # Créer une commande d'abord
        order_data = {
            "customer_name": "Charlie Davis",
            "customer_address": "654 Maple Dr"
        }
        order_response = client.post('/orders',
                                     data=json.dumps(order_data),
                                     content_type='application/json')
        order_id = json.loads(order_response.data)['order_id']
        
        # Créer une livraison
        delivery_data = {
            "order_id": order_id,
            "driver_name": "Mike Driver"
        }
        response = client.post('/deliveries',
                              data=json.dumps(delivery_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['driver_name'] == "Mike Driver"
        assert data['status'] == "assigned"
        assert 'delivery_id' in data
    
    def test_start_delivery(self, client, reset_stores):
        """Test le démarrage d'une livraison"""
        # Créer commande et livraison
        order_data = {
            "customer_name": "Diana Evans",
            "customer_address": "987 Birch Ln"
        }
        order_response = client.post('/orders',
                                     data=json.dumps(order_data),
                                     content_type='application/json')
        order_id = json.loads(order_response.data)['order_id']
        
        delivery_data = {
            "order_id": order_id,
            "driver_name": "Sarah Driver"
        }
        delivery_response = client.post('/deliveries',
                                        data=json.dumps(delivery_data),
                                        content_type='application/json')
        delivery_id = json.loads(delivery_response.data)['delivery_id']
        
        # Démarrer la livraison
        response = client.patch(f'/deliveries/{delivery_id}/start')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == "in_transit"
        assert data['started_at'] is not None
    
    def test_complete_delivery(self, client, reset_stores):
        """Test la complétion d'une livraison"""
        # Créer commande et livraison
        order_data = {
            "customer_name": "Frank Green",
            "customer_address": "147 Cedar St"
        }
        order_response = client.post('/orders',
                                     data=json.dumps(order_data),
                                     content_type='application/json')
        order_id = json.loads(order_response.data)['order_id']
        
        delivery_data = {
            "order_id": order_id,
            "driver_name": "Tom Driver"
        }
        delivery_response = client.post('/deliveries',
                                        data=json.dumps(delivery_data),
                                        content_type='application/json')
        delivery_id = json.loads(delivery_response.data)['delivery_id']
        
        # Démarrer puis compléter
        client.patch(f'/deliveries/{delivery_id}/start')
        response = client.patch(f'/deliveries/{delivery_id}/complete')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == "delivered"
        assert data['completed_at'] is not None
    
    def test_update_delivery_location(self, client, reset_stores):
        """Test la mise à jour de la position GPS"""
        # Créer commande et livraison
        order_data = {
            "customer_name": "Grace Hill",
            "customer_address": "258 Willow Way"
        }
        order_response = client.post('/orders',
                                     data=json.dumps(order_data),
                                     content_type='application/json')
        order_id = json.loads(order_response.data)['order_id']
        
        delivery_data = {
            "order_id": order_id,
            "driver_name": "Emma Driver"
        }
        delivery_response = client.post('/deliveries',
                                        data=json.dumps(delivery_data),
                                        content_type='application/json')
        delivery_id = json.loads(delivery_response.data)['delivery_id']
        
        # Mettre à jour la position
        location_data = {
            "latitude": 48.8566,
            "longitude": 2.3522
        }
        response = client.patch(f'/deliveries/{delivery_id}/location',
                               data=json.dumps(location_data),
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['current_latitude'] == 48.8566
        assert data['current_longitude'] == 2.3522


class TestEndToEndFlow:
    """Test du flux complet de bout en bout"""
    
    def test_complete_pizza_delivery_flow(self, client, reset_stores):
        """Test le flux complet : Créer pizza → Commande → Livraison → Livrer"""
        
        # 1. Créer une pizza
        pizza_data = {
            "name": "Supreme",
            "size": "Large",
            "price": 18.99,
            "toppings": ["pepperoni", "mushrooms", "olives"]
        }
        pizza_response = client.post('/pizzas',
                                     data=json.dumps(pizza_data),
                                     content_type='application/json')
        assert pizza_response.status_code == 201
        pizza_id = json.loads(pizza_response.data)['pizza_id']
        
        # 2. Créer une commande
        order_data = {
            "customer_name": "Test Customer",
            "customer_address": "123 Test Street"
        }
        order_response = client.post('/orders',
                                     data=json.dumps(order_data),
                                     content_type='application/json')
        assert order_response.status_code == 201
        order_id = json.loads(order_response.data)['order_id']
        
        # 3. Ajouter la pizza à la commande
        add_pizza_response = client.post(f'/orders/{order_id}/pizzas',
                                         data=json.dumps({"pizza_id": pizza_id}),
                                         content_type='application/json')
        assert add_pizza_response.status_code == 200
        order_data = json.loads(add_pizza_response.data)
        assert len(order_data['pizzas']) == 1
        assert order_data['total'] == 18.99
        
        # 4. Mettre à jour le statut de la commande
        status_response = client.patch(f'/orders/{order_id}/status',
                                       data=json.dumps({"status": "preparing"}),
                                       content_type='application/json')
        assert status_response.status_code == 200
        
        # 5. Créer une livraison
        delivery_data = {
            "order_id": order_id,
            "driver_name": "Test Driver"
        }
        delivery_response = client.post('/deliveries',
                                        data=json.dumps(delivery_data),
                                        content_type='application/json')
        assert delivery_response.status_code == 201
        delivery_id = json.loads(delivery_response.data)['delivery_id']
        
        # 6. Démarrer la livraison
        start_response = client.patch(f'/deliveries/{delivery_id}/start')
        assert start_response.status_code == 200
        delivery_data = json.loads(start_response.data)
        assert delivery_data['status'] == "in_transit"
        
        # 7. Mettre à jour la position
        location_response = client.patch(f'/deliveries/{delivery_id}/location',
                                         data=json.dumps({
                                             "latitude": 48.8566,
                                             "longitude": 2.3522
                                         }),
                                         content_type='application/json')
        assert location_response.status_code == 200
        
        # 8. Compléter la livraison
        complete_response = client.patch(f'/deliveries/{delivery_id}/complete')
        assert complete_response.status_code == 200
        final_delivery = json.loads(complete_response.data)
        assert final_delivery['status'] == "delivered"
        assert final_delivery['completed_at'] is not None
        
        # Vérifier la commande finale
        final_order_response = client.get(f'/orders/{order_id}')
        assert final_order_response.status_code == 200
        final_order = json.loads(final_order_response.data)
        assert final_order['total'] == 18.99
        
        print("\n✅ Flux E2E complet réussi!")
