import pytest
from app.models import Pizza


class TestPizza:
    """Tests pour la classe Pizza"""
    
    def test_pizza_creation(self):
        """Test la création d'une pizza avec nom, taille et prix"""
        pizza = Pizza(name="Margherita", size="Medium", price=12.99)
        
        assert pizza.name == "Margherita"
        assert pizza.size == "Medium"
        assert pizza.price.amount == 12.99

    def test_pizza_with_toppings(self):
        """Test la création d'une pizza avec des garnitures"""
        pizza = Pizza(
            name="Supreme",
            size="Large",
            price=18.99,
            toppings=["pepperoni", "mushrooms", "olives"]
        )
        
        assert pizza.name == "Supreme"
        assert len(pizza.toppings) == 3
        assert "pepperoni" in pizza.toppings
    
    def test_pizza_add_topping(self):
        """Test l'ajout d'une garniture à une pizza"""
        pizza = Pizza(name="Custom", size="Small", price=10.99)
        pizza.add_topping("extra cheese")
        
        assert "extra cheese" in pizza.toppings
        assert len(pizza.toppings) == 1
    
    def test_pizza_remove_topping(self):
        """Test la suppression d'une garniture"""
        pizza = Pizza(
            name="Veggie",
            size="Medium",
            price=14.99,
            toppings=["tomatoes", "peppers", "onions"]
        )
        pizza.remove_topping("peppers")
        
        assert "peppers" not in pizza.toppings
        assert len(pizza.toppings) == 2
    
    def test_pizza_to_dict(self):
        """Test la conversion d'une pizza en dictionnaire"""
        pizza = Pizza(
            name="Hawaiian",
            size="Large",
            price=16.99,
            toppings=["ham", "pineapple"]
        )
        pizza_dict = pizza.to_dict()
        
        assert pizza_dict["name"] == "Hawaiian"
        assert pizza_dict["size"] == "Large"
        assert pizza_dict["price"] == 16.99
        assert pizza_dict["toppings"] == ["ham", "pineapple"]
    
    def test_pizza_invalid_size(self):
        """Test qu'une taille invalide lève une exception"""
        with pytest.raises(ValueError):
            Pizza(name="Test", size="Huge", price=10.99)
    
    def test_pizza_invalid_price(self):
        """Test qu'un prix négatif lève une exception"""
        with pytest.raises(ValueError):
            Pizza(name="Test", size="Medium", price=-5.00)
