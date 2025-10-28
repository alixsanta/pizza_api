import pytest
from datetime import datetime
from app.models import Delivery, Order, Pizza


class TestDelivery:
    """Tests pour la classe Delivery"""
    
    def test_delivery_creation(self):
        """Test la création d'une livraison"""
        order = Order(customer_name="John Doe", customer_address="123 Main St")
        delivery = Delivery(order=order, driver_name="Mike Driver")
        
        assert delivery.order == order
        assert delivery.driver_name == "Mike Driver"
        assert delivery.status == "assigned"
        assert delivery.delivery_id is not None
    
    def test_delivery_start_delivery(self):
        """Test le démarrage d'une livraison"""
        order = Order(customer_name="Jane Smith", customer_address="456 Oak Ave")
        pizza = Pizza(name="Margherita", size="Medium", price=12.99)
        order.add_pizza(pizza)
        
        delivery = Delivery(order=order, driver_name="Sarah Driver")
        delivery.start_delivery()
        
        assert delivery.status == "in_transit"
        assert delivery.started_at is not None
    
    def test_delivery_complete_delivery(self):
        """Test la complétion d'une livraison"""
        order = Order(customer_name="Bob Johnson", customer_address="789 Elm St")
        pizza = Pizza(name="Pepperoni", size="Large", price=15.99)
        order.add_pizza(pizza)
        
        delivery = Delivery(order=order, driver_name="Tom Driver")
        delivery.start_delivery()
        delivery.complete_delivery()
        
        assert delivery.status == "delivered"
        assert delivery.completed_at is not None
    
    def test_delivery_cannot_complete_without_starting(self):
        """Test qu'on ne peut pas compléter une livraison non démarrée"""
        order = Order(customer_name="Alice Brown", customer_address="321 Pine Rd")
        delivery = Delivery(order=order, driver_name="Lisa Driver")
        
        with pytest.raises(ValueError):
            delivery.complete_delivery()
    
    def test_delivery_calculate_duration(self):
        """Test le calcul de la durée de livraison"""
        order = Order(customer_name="Charlie Davis", customer_address="654 Maple Dr")
        pizza = Pizza(name="Supreme", size="Large", price=18.99)
        order.add_pizza(pizza)
        
        delivery = Delivery(order=order, driver_name="Jack Driver")
        delivery.start_delivery()
        delivery.complete_delivery()
        
        duration = delivery.calculate_duration()
        assert duration is not None
        assert duration >= 0
    
    def test_delivery_update_location(self):
        """Test la mise à jour de la position du livreur"""
        order = Order(customer_name="Diana Evans", customer_address="987 Birch Ln")
        delivery = Delivery(order=order, driver_name="Emma Driver")
        
        delivery.update_location(latitude=48.8566, longitude=2.3522)
        
        assert delivery.current_latitude == 48.8566
        assert delivery.current_longitude == 2.3522
    
    def test_delivery_cancel_delivery(self):
        """Test l'annulation d'une livraison"""
        order = Order(customer_name="Frank Green", customer_address="147 Cedar St")
        delivery = Delivery(order=order, driver_name="Chris Driver")
        
        delivery.cancel_delivery("Customer not available")
        
        assert delivery.status == "cancelled"
        assert delivery.cancellation_reason == "Customer not available"
    
    def test_delivery_to_dict(self):
        """Test la conversion d'une livraison en dictionnaire"""
        order = Order(customer_name="Grace Hill", customer_address="258 Willow Way")
        pizza = Pizza(name="Hawaiian", size="Medium", price=14.99)
        order.add_pizza(pizza)
        
        delivery = Delivery(order=order, driver_name="David Driver")
        delivery_dict = delivery.to_dict()
        
        assert delivery_dict["driver_name"] == "David Driver"
        assert delivery_dict["status"] == "assigned"
        assert "order" in delivery_dict
        assert delivery_dict["order"]["customer_name"] == "Grace Hill"
    
    def test_delivery_estimated_time(self):
        """Test le calcul du temps estimé de livraison"""
        order = Order(customer_name="Henry Iron", customer_address="369 Spruce Blvd")
        delivery = Delivery(order=order, driver_name="Nina Driver")
        
        estimated_time = delivery.get_estimated_time()
        
        assert estimated_time is not None
        assert estimated_time > 0
    
    def test_delivery_invalid_status_transition(self):
        """Test qu'une transition de statut invalide lève une exception"""
        order = Order(customer_name="Test User", customer_address="Test Address")
        delivery = Delivery(order=order, driver_name="Test Driver")
        
        delivery.start_delivery()
        
        with pytest.raises(ValueError):
            delivery.start_delivery()  # Ne peut pas redémarrer
