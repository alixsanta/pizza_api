"""
Classe Delivery pour représenter une livraison
"""
import uuid
from datetime import datetime
from typing import Optional


class Delivery:
    """Représente une livraison de commande"""
    
    def __init__(self, order, driver_name: str):
        """
        Initialise une livraison
        
        Args:
            order: Instance de Order à livrer
            driver_name: Nom du livreur
        """
        self.delivery_id = str(uuid.uuid4())
        self.order = order
        self.driver_name = driver_name
        self.status = "assigned"
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.current_latitude: Optional[float] = None
        self.current_longitude: Optional[float] = None
        self.cancellation_reason: Optional[str] = None
    
    def start_delivery(self) -> None:
        """
        Démarre la livraison
        
        Raises:
            ValueError: Si la livraison a déjà été démarrée
        """
        if self.status == "in_transit":
            raise ValueError("Delivery has already been started")
        
        if self.status == "delivered":
            raise ValueError("Delivery has already been completed")
        
        if self.status == "cancelled":
            raise ValueError("Cannot start a cancelled delivery")
        
        self.status = "in_transit"
        self.started_at = datetime.now()
    
    def complete_delivery(self) -> None:
        """
        Complète la livraison
        
        Raises:
            ValueError: Si la livraison n'a pas été démarrée
        """
        if self.status != "in_transit":
            raise ValueError("Delivery must be started before it can be completed")
        
        self.status = "delivered"
        self.completed_at = datetime.now()
    
    def calculate_duration(self) -> Optional[float]:
        """
        Calcule la durée de la livraison en secondes
        
        Returns:
            La durée en secondes ou None si la livraison n'est pas terminée
        """
        if self.started_at is None or self.completed_at is None:
            return None
        
        duration = (self.completed_at - self.started_at).total_seconds()
        return duration
    
    def update_location(self, latitude: float, longitude: float) -> None:
        """
        Met à jour la position actuelle du livreur
        
        Args:
            latitude: Latitude actuelle
            longitude: Longitude actuelle
        """
        self.current_latitude = latitude
        self.current_longitude = longitude
    
    def cancel_delivery(self, reason: str) -> None:
        """
        Annule la livraison
        
        Args:
            reason: Raison de l'annulation
        """
        self.status = "cancelled"
        self.cancellation_reason = reason
    
    def get_estimated_time(self) -> int:
        """
        Calcule le temps estimé de livraison en minutes
        
        Returns:
            Temps estimé en minutes (par défaut 30 minutes)
        """
        # Implémentation simple : retourne un temps estimé fixe
        # Dans une vraie application, cela pourrait être basé sur la distance, le trafic, etc.
        return 30
    
    def to_dict(self) -> dict:
        """
        Convertit la livraison en dictionnaire
        
        Returns:
            Dictionnaire contenant les informations de la livraison
        """
        return {
            "delivery_id": self.delivery_id,
            "order": self.order.to_dict(),
            "driver_name": self.driver_name,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "current_latitude": self.current_latitude,
            "current_longitude": self.current_longitude,
            "cancellation_reason": self.cancellation_reason
        }
