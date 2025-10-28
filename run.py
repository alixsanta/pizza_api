"""
Point d'entrée pour lancer l'application Flask
"""
from app.app import app

if __name__ == '__main__':
    print("🍕 Pizza Delivery API Starting...")
    print("📍 Server running on http://localhost:5000")
    print("📚 Health check: http://localhost:5000/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
