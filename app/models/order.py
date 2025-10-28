"""
Classe Order pour représenter une commande
"""
import uuid
from datetime import datetime
from typing import List


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
    
    def calculate_total(self) -> float:
        """
        Calcule le prix total de la commande
        
        Returns:
            Le prix total de toutes les pizzas
        """
        return sum(pizza.price for pizza in self.pizzas)
    
    def update_status(self, new_status: str) -> None:
        """
        Met à jour le statut de la commande
        
        Args:
            new_status: Le nouveau statut
        
        Raises:
            ValueError: Si le statut est invalide
        """
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status. Must be one of {self.VALID_STATUSES}")
        self.status = new_status
    
    def to_dict(self) -> dict:
        """
        Convertit la commande en dictionnaire
        
        Returns:
            Dictionnaire contenant les informations de la commande
        """
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "customer_address": self.customer_address,
            "status": self.status,
            "pizzas": [pizza.to_dict() for pizza in self.pizzas],
            "total": self.calculate_total(),
            "created_at": self.created_at.isoformat()
        }
