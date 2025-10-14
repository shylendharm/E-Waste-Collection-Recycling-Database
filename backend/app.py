import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from backend.routes import register_routes
from backend.database import create_tables

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.secret_key = 'your-secret-key-here'  # Change this in production
    
    # Create tables if they don't exist
    create_tables()
    
    # Register routes
    register_routes(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    # Make sure the database directory exists
    os.makedirs('../database', exist_ok=True)
    
    # Create tables
    create_tables()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)