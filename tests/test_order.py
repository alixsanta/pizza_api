import pytest
from datetime import datetime
from app.models import Order, Pizza


class TestOrder:
    """Tests pour la classe Order"""
    
    def test_order_creation(self):
        """Test la création d'une commande basique"""
        order = Order(customer_name="John Doe", customer_address="123 Main St")
        
        assert order.customer_name == "John Doe"
        assert order.customer_address == "123 Main St"
        assert order.status == "pending"
        assert order.pizzas == []
        assert order.order_id is not None
    
    def test_order_add_pizza(self):
        """Test l'ajout d'une pizza à une commande"""
        order = Order(customer_name="Jane Smith", customer_address="456 Oak Ave")
        pizza = Pizza(name="Pepperoni", size="Large", price=15.99)
        
        order.add_pizza(pizza)
        
        assert len(order.pizzas) == 1
        assert order.pizzas[0].name == "Pepperoni"
    
    def test_order_add_multiple_pizzas(self):
        """Test l'ajout de plusieurs pizzas"""
        order = Order(customer_name="Bob Johnson", customer_address="789 Elm St")
        pizza1 = Pizza(name="Margherita", size="Medium", price=12.99)
        pizza2 = Pizza(name="Supreme", size="Large", price=18.99)
        
        order.add_pizza(pizza1)
        order.add_pizza(pizza2)
        
        assert len(order.pizzas) == 2
    
    def test_order_remove_pizza(self):
        """Test la suppression d'une pizza de la commande"""
        order = Order(customer_name="Alice Brown", customer_address="321 Pine Rd")
        pizza1 = Pizza(name="Hawaiian", size="Medium", price=14.99)
        pizza2 = Pizza(name="Veggie", size="Small", price=11.99)
        
        order.add_pizza(pizza1)
        order.add_pizza(pizza2)
        order.remove_pizza(0)
        
        assert len(order.pizzas) == 1
        assert order.pizzas[0].name == "Veggie"
    
    def test_order_calculate_total(self):
        """Test le calcul du total de la commande"""
        order = Order(customer_name="Charlie Davis", customer_address="654 Maple Dr")
        pizza1 = Pizza(name="Margherita", size="Medium", price=12.99)
        pizza2 = Pizza(name="Pepperoni", size="Large", price=15.99)
        
        order.add_pizza(pizza1)
        order.add_pizza(pizza2)
        
        total = order.calculate_total()
        assert total == 28.98
    
    def test_order_update_status(self):
        """Test la mise à jour du statut de la commande"""
        order = Order(customer_name="Diana Evans", customer_address="987 Birch Ln")
        
        order.update_status("preparing")
        assert order.status == "preparing"
        
        order.update_status("ready")
        assert order.status == "ready"
    
    def test_order_invalid_status(self):
        """Test qu'un statut invalide lève une exception"""
        order = Order(customer_name="Test User", customer_address="Test Address")
        
        with pytest.raises(ValueError):
            order.update_status("invalid_status")
    
    def test_order_to_dict(self):
        """Test la conversion d'une commande en dictionnaire"""
        order = Order(customer_name="Frank Green", customer_address="147 Cedar St")
        pizza = Pizza(name="Supreme", size="Large", price=18.99)
        order.add_pizza(pizza)
        
        order_dict = order.to_dict()
        
        assert order_dict["customer_name"] == "Frank Green"
        assert order_dict["customer_address"] == "147 Cedar St"
        assert order_dict["status"] == "pending"
        assert len(order_dict["pizzas"]) == 1
        assert order_dict["total"] == 18.99
    
    def test_order_created_at(self):
        """Test que la date de création est enregistrée"""
        order = Order(customer_name="Grace Hill", customer_address="258 Willow Way")
        
        assert order.created_at is not None
        assert isinstance(order.created_at, datetime)
