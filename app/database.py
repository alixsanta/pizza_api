"""
Configuration de la base de données SQLAlchemy
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def init_db(app):
    """
    Initialise la base de données avec l'application Flask
    Peuple automatiquement la base si elle est vide

    Args:
        app: Instance de l'application Flask
    """
    db.init_app(app)

    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        print("✅ Base de données initialisée avec succès")

        # Peupler la base si elle est vide
        from app.seeds import is_database_empty, seed_all

        if is_database_empty():
            print("\n🌱 Base de données vide détectée - Peuplement automatique...")
            stats = seed_all()
            print(f"\n📊 Peuplement terminé :")
            print(f"   - {stats['pizzas']} pizzas ajoutées")
            print(f"   - {stats['orders']} commandes ajoutées")
            print("="*50)
        else:
            print("📊 Base de données déjà peuplée - Aucune action nécessaire")



