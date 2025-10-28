"""
Classe Price pour représenter un prix avec devise
"""
from typing import Dict


class Price:
    """Représente un prix avec montant et devise"""
    
    VALID_CURRENCIES = ["EUR", "USD", "GBP", "CAD"]
    CURRENCY_SYMBOLS = {
        "EUR": "€",
        "USD": "$",
        "GBP": "£",
        "CAD": "C$"
    }
    
    def __init__(self, amount: float, currency: str = "EUR"):
        """
        Initialise un prix
        
        Args:
            amount: Montant du prix
            currency: Devise (EUR par défaut)
        
        Raises:
            ValueError: Si le montant est négatif ou la devise invalide
        """
        if amount < 0:
            raise ValueError("Price amount cannot be negative")
        
        if currency not in self.VALID_CURRENCIES:
            raise ValueError(f"Invalid currency. Must be one of {self.VALID_CURRENCIES}")
        
        self.amount = round(amount, 2)  # Arrondir à 2 décimales
        self.currency = currency
    
    def __add__(self, other):
        """Addition de deux prix"""
        if not isinstance(other, Price):
            raise TypeError("Can only add Price objects together")
        
        if self.currency != other.currency:
            raise ValueError("Cannot add prices with different currencies")
        
        return Price(self.amount + other.amount, self.currency)
    
    def __sub__(self, other):
        """Soustraction de deux prix"""
        if not isinstance(other, Price):
            raise TypeError("Can only subtract Price objects")
        
        if self.currency != other.currency:
            raise ValueError("Cannot subtract prices with different currencies")
        
        result_amount = self.amount - other.amount
        if result_amount < 0:
            raise ValueError("Subtraction would result in negative price")
        
        return Price(result_amount, self.currency)
    
    def __mul__(self, multiplier):
        """Multiplication d'un prix par un nombre"""
        if not isinstance(multiplier, (int, float)):
            raise TypeError("Can only multiply by numbers")
        
        return Price(self.amount * multiplier, self.currency)
    
    def __rmul__(self, multiplier):
        """Multiplication inverse (nombre * prix)"""
        return self.__mul__(multiplier)
    
    def __gt__(self, other):
        """Comparaison : plus grand que"""
        if not isinstance(other, Price):
            raise TypeError("Can only compare with Price objects")
        
        if self.currency != other.currency:
            raise ValueError("Cannot compare prices with different currencies")
        
        return self.amount > other.amount
    
    def __lt__(self, other):
        """Comparaison : plus petit que"""
        if not isinstance(other, Price):
            raise TypeError("Can only compare with Price objects")
        
        if self.currency != other.currency:
            raise ValueError("Cannot compare prices with different currencies")
        
        return self.amount < other.amount
    
    def __eq__(self, other):
        """Comparaison : égal à"""
        if not isinstance(other, Price):
            return False
        
        return self.amount == other.amount and self.currency == other.currency
    
    def __str__(self):
        """Représentation en string"""
        return self.format()
    
    def __repr__(self):
        """Représentation pour debug"""
        return f"Price(amount={self.amount}, currency='{self.currency}')"
    
    def format(self, with_symbol: bool = False) -> str:
        """
        Formate le prix en string
        
        Args:
            with_symbol: Si True, utilise le symbole de la devise
        
        Returns:
            Prix formaté
        """
        if with_symbol:
            symbol = self.CURRENCY_SYMBOLS.get(self.currency, self.currency)
            if self.currency == "EUR":
                return f"{self.amount:.2f} {symbol}"
            else:
                return f"{symbol}{self.amount:.2f}"
        
        return f"{self.amount:.2f} {self.currency}"
    
    def round(self, decimals: int = 2):
        """
        Arrondit le prix
        
        Args:
            decimals: Nombre de décimales
        
        Returns:
            Nouveau prix arrondi
        """
        return Price(round(self.amount, decimals), self.currency)
    
    def apply_discount(self, percentage: float):
        """
        Applique une réduction en pourcentage
        
        Args:
            percentage: Pourcentage de réduction (ex: 20 pour 20%)
        
        Returns:
            Nouveau prix avec réduction appliquée
        """
        if percentage < 0 or percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        
        discount_amount = self.amount * (percentage / 100)
        new_amount = self.amount - discount_amount
        
        return Price(new_amount, self.currency)
    
    def apply_tax(self, percentage: float):
        """
        Applique une taxe en pourcentage
        
        Args:
            percentage: Pourcentage de taxe (ex: 20 pour 20%)
        
        Returns:
            Nouveau prix avec taxe appliquée
        """
        if percentage < 0:
            raise ValueError("Tax percentage cannot be negative")
        
        tax_amount = self.amount * (percentage / 100)
        new_amount = self.amount + tax_amount
        
        return Price(new_amount, self.currency)
    
    def to_dict(self) -> Dict:
        """
        Convertit le prix en dictionnaire
        
        Returns:
            Dictionnaire contenant le montant et la devise
        """
        return {
            "amount": self.amount,
            "currency": self.currency
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """
        Crée un prix depuis un dictionnaire
        
        Args:
            data: Dictionnaire avec 'amount' et 'currency'
        
        Returns:
            Instance de Price
        """
        return cls(
            amount=data.get("amount", 0),
            currency=data.get("currency", "EUR")
        )
