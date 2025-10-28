import pytest
from app.models import Price


class TestPrice:
    """Tests pour la classe Price"""
    
    def test_price_creation(self):
        """Test la création d'un prix basique"""
        price = Price(amount=12.99, currency="EUR")
        
        assert price.amount == 12.99
        assert price.currency == "EUR"
    
    def test_price_default_currency(self):
        """Test que la devise par défaut est EUR"""
        price = Price(amount=15.99)
        
        assert price.currency == "EUR"
    
    def test_price_negative_amount(self):
        """Test qu'un montant négatif lève une exception"""
        with pytest.raises(ValueError):
            Price(amount=-10.00)
    
    def test_price_zero_amount(self):
        """Test qu'un montant de 0 est accepté"""
        price = Price(amount=0.00)
        
        assert price.amount == 0.00
    
    def test_price_invalid_currency(self):
        """Test qu'une devise invalide lève une exception"""
        with pytest.raises(ValueError):
            Price(amount=10.00, currency="XXX")
    
    def test_price_add(self):
        """Test l'addition de deux prix"""
        price1 = Price(amount=10.99, currency="EUR")
        price2 = Price(amount=5.50, currency="EUR")
        
        total = price1 + price2
        
        assert total.amount == 16.49
        assert total.currency == "EUR"
    
    def test_price_add_different_currencies(self):
        """Test qu'on ne peut pas additionner des devises différentes"""
        price1 = Price(amount=10.99, currency="EUR")
        price2 = Price(amount=5.50, currency="USD")
        
        with pytest.raises(ValueError):
            total = price1 + price2
    
    def test_price_multiply(self):
        """Test la multiplication d'un prix par un nombre"""
        price = Price(amount=10.00, currency="EUR")
        
        total = price * 3
        
        assert total.amount == 30.00
        assert total.currency == "EUR"
    
    def test_price_subtract(self):
        """Test la soustraction de deux prix"""
        price1 = Price(amount=20.00, currency="EUR")
        price2 = Price(amount=7.50, currency="EUR")
        
        result = price1 - price2
        
        assert result.amount == 12.50
        assert result.currency == "EUR"
    
    def test_price_comparison_greater(self):
        """Test la comparaison de prix (plus grand)"""
        price1 = Price(amount=20.00, currency="EUR")
        price2 = Price(amount=10.00, currency="EUR")
        
        assert price1 > price2
        assert not price2 > price1
    
    def test_price_comparison_equal(self):
        """Test l'égalité de prix"""
        price1 = Price(amount=15.99, currency="EUR")
        price2 = Price(amount=15.99, currency="EUR")
        
        assert price1 == price2
    
    def test_price_format(self):
        """Test le formatage d'un prix"""
        price = Price(amount=12.99, currency="EUR")
        
        assert price.format() == "12.99 EUR"
    
    def test_price_format_usd(self):
        """Test le formatage avec symbole USD"""
        price = Price(amount=19.99, currency="USD")
        
        formatted = price.format(with_symbol=True)
        assert "$" in formatted
    
    def test_price_to_dict(self):
        """Test la conversion en dictionnaire"""
        price = Price(amount=25.50, currency="EUR")
        
        price_dict = price.to_dict()
        
        assert price_dict["amount"] == 25.50
        assert price_dict["currency"] == "EUR"
    
    def test_price_from_dict(self):
        """Test la création depuis un dictionnaire"""
        price_data = {"amount": 18.99, "currency": "USD"}
        
        price = Price.from_dict(price_data)
        
        assert price.amount == 18.99
        assert price.currency == "USD"
    
    def test_price_round(self):
        """Test l'arrondi d'un prix"""
        # Note: Price constructor already rounds to 2 decimals
        # So we need to test rounding from 2 to 0 or 1 decimal
        price = Price(amount=12.99, currency="EUR")

        rounded = price.round(0)

        assert rounded.amount == 13.00
    
    def test_price_apply_discount(self):
        """Test l'application d'une réduction en pourcentage"""
        price = Price(amount=100.00, currency="EUR")
        
        discounted = price.apply_discount(20)  # 20% de réduction
        
        assert discounted.amount == 80.00
    
    def test_price_apply_tax(self):
        """Test l'application d'une taxe"""
        price = Price(amount=100.00, currency="EUR")
        
        with_tax = price.apply_tax(20)  # 20% de taxe (TVA)
        
        assert with_tax.amount == 120.00
    
    def test_price_string_representation(self):
        """Test la représentation en string"""
        price = Price(amount=15.99, currency="EUR")
        
        assert str(price) == "15.99 EUR"
