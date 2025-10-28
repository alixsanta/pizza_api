"""
Classe Pizza pour représenter une pizza
"""
from .price import Price
from typing import Union


class Pizza:
    """Représente une pizza avec ses caractéristiques"""
    
    VALID_SIZES = ["Small", "Medium", "Large"]
    
    def __init__(self, name: str, size: str, price: Union[float, Price], toppings: list = None, currency: str = "EUR"):
        """
        Initialise une pizza
        
        Args:
            name: Nom de la pizza
            size: Taille de la pizza (Small, Medium, Large)
            price: Prix de la pizza (float ou Price)
            toppings: Liste des garnitures (optionnel)
            currency: Devise (si price est un float)
        
        Raises:
            ValueError: Si la taille est invalide ou le prix est négatif
        """
        if size not in self.VALID_SIZES:
            raise ValueError(f"Invalid size. Must be one of {self.VALID_SIZES}")
        
        # Convertir le prix en objet Price si c'est un float
        if isinstance(price, (int, float)):
            if price < 0:
                raise ValueError("Price cannot be negative")
            self.price = Price(amount=price, currency=currency)
        elif isinstance(price, Price):
            self.price = price
        else:
            raise TypeError("Price must be a number or Price object")
        
        self.name = name
        self.size = size
        self.toppings = toppings if toppings is not None else []
    
    def add_topping(self, topping: str) -> None:
        """
        Ajoute une garniture à la pizza
        
        Args:
            topping: La garniture à ajouter
        """
        self.toppings.append(topping)
    
    def remove_topping(self, topping: str) -> None:
        """
        Retire une garniture de la pizza
        
        Args:
            topping: La garniture à retirer
        """
        if topping in self.toppings:
            self.toppings.remove(topping)
    
    def to_dict(self) -> dict:
        """
        Convertit la pizza en dictionnaire
        
        Returns:
            Dictionnaire contenant les informations de la pizza
        """
        return {
            "name": self.name,
            "size": self.size,
            "price": self.price.amount,  # Convertir Price en float pour compatibilité
            "currency": self.price.currency,
            "toppings": self.toppings
        }
