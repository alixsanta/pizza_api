"""
Classe Order pour représenter une commande
"""
import uuid
from datetime import datetime
from typing import List
from .price import Price


class Order:
    """Représente une commande de pizzas"""
    
    VALID_STATUSES = ["pending", "preparing", "ready", "out_for_delivery", "delivered", "cancelled"]
    
    def __init__(self, customer_name: str, customer_address: str):
        """
        Initialise une commande
        
        Args:
            customer_name: Nom du client
            customer_address: Adresse de livraison
        """
        self.order_id = str(uuid.uuid4())
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.status = "pending"
        self.pizzas: List = []
        self.created_at = datetime.now()
    
    def add_pizza(self, pizza) -> None:
        """
        Ajoute une pizza à la commande
        
        Args:
            pizza: Instance de Pizza à ajouter
        """
        self.pizzas.append(pizza)
    
    def remove_pizza(self, index: int) -> None:
        """
        Retire une pizza de la commande par son index
        
        Args:
            index: Index de la pizza à retirer
        """
        if 0 <= index < len(self.pizzas):
            self.pizzas.pop(index)
    
    def calculate_total(self) -> Price:
        """
        Calcule le prix total de la commande
        
        Returns:
            Le prix total de toutes les pizzas (objet Price)
        
        Raises:
            ValueError: Si la commande est vide ou a des devises différentes
        """
        if not self.pizzas:
            # Retourner un prix de 0 par défaut
            return Price(amount=0, currency="EUR")
        
        # Vérifier que toutes les pizzas ont la même devise
        first_currency = self.pizzas[0].price.currency
        for pizza in self.pizzas:
            if pizza.price.currency != first_currency:
                raise ValueError("All pizzas must have the same currency")
        
        # Calculer le total
        total = Price(amount=0, currency=first_currency)
        for pizza in self.pizzas:
            total = total + pizza.price
        
        return total
    
    def is_valid(self) -> bool:
        """
        Vérifie si la commande est valide (a au moins une pizza)
        
        Returns:
            True si la commande a au moins une pizza, False sinon
        """
        return len(self.pizzas) > 0
    
    def validate(self) -> None:
        """
        Valide la commande avant traitement
        
        Raises:
            ValueError: Si la commande n'a pas de pizza
        """
        if not self.is_valid():
            raise ValueError("Order must have at least one pizza to be valid")
    
    def update_status(self, new_status: str) -> None:
        """
        Met à jour le statut de la commande
        
        Args:
            new_status: Le nouveau statut
        
        Raises:
            ValueError: Si le statut est invalide ou si la commande n'est pas valide
        """
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status. Must be one of {self.VALID_STATUSES}")
        
        # Validation obligatoire pour certains statuts
        if new_status in ["preparing", "ready", "out_for_delivery", "delivered"]:
            self.validate()
        
        self.status = new_status
    
    def to_dict(self) -> dict:
        """
        Convertit la commande en dictionnaire
        
        Returns:
            Dictionnaire contenant les informations de la commande
        """
        total = self.calculate_total()
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "customer_address": self.customer_address,
            "status": self.status,
            "pizzas": [pizza.to_dict() for pizza in self.pizzas],
            "total": total.amount,
            "currency": total.currency,
            "is_valid": self.is_valid(),
            "created_at": self.created_at.isoformat()
        }
