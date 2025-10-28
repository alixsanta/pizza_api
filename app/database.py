"""
Configuration de la base de données SQLAlchemy
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def init_db(app):
    """
    Initialise la base de données avec l'application Flask

    Args:
        app: Instance de l'application Flask
    """
    db.init_app(app)

    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        print("✅ Base de données initialisée avec succès")

