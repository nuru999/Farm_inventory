"""
Farm Inventory Management System - Improved Backend
Production-ready Flask application with PostgreSQL support
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import models and blueprints
from models import db, InventoryModel
from blueprints import inventory_bp, pages_bp
from config import config_by_name

# =======================
# APP INITIALIZATION
# =======================

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    config_class = config_by_name.get(config_name, config_by_name['development'])
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(inventory_bp)
    app.register_blueprint(pages_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app


# Create app instance (using environment variable or default)
app = create_app(os.environ.get('FLASK_ENV', 'development'))


# =======================
# PAGE ROUTES (Frontend)
# =======================

@app.route('/')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')


@app.route('/inventory')
def inventory():
    """Inventory management page"""
    return render_template('inventory.html')


@app.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html')


# =======================
# ERROR HANDLERS
# =======================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return {
        'status': 'error',
        'message': 'Resource not found',
        'code': 404
    }, 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return {
        'status': 'error',
        'message': 'Internal server error',
        'code': 500
    }, 500


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return {
        'status': 'error',
        'message': 'Bad request',
        'code': 400
    }, 400


# =======================
# CLI COMMANDS (optional)
# =======================

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized.')


@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    sample_items = [
        InventoryModel(
            Item='Maize Seeds',
            Category='Seeds',
            Quantity=100,
            Units_of_Measurement='kg',
            Unit_Cost=5.50,
            Supplier='AgriSupply Co.',
            Purchase_Date=None,
            Expiry_Date=None
        ),
        InventoryModel(
            Item='Fertilizer NPK',
            Category='Fertilizers',
            Quantity=500,
            Units_of_Measurement='kg',
            Unit_Cost=2.75,
            Supplier='ChemicalWorks Ltd.',
            Purchase_Date=None,
            Expiry_Date=None
        ),
        InventoryModel(
            Item='Irrigation Pipe',
            Category='Equipment',
            Quantity=50,
            Units_of_Measurement='meters',
            Unit_Cost=15.00,
            Supplier='Hardware Hub',
            Purchase_Date=None,
            Expiry_Date=None
        ),
    ]
    
    for item in sample_items:
        if not InventoryModel.query.filter_by(Item=item.Item).first():
            db.session.add(item)
    
    db.session.commit()
    print('Database seeded with sample data.')


# =======================
# RUN APP
# =======================

if __name__ == '__main__':
    # Development server
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print(f"🌱 Farm Inventory Management System")
    print(f"📍 Running on {host}:{port}")
    print(f"🔧 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"💾 Database: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1] if '@' in app.config['SQLALCHEMY_DATABASE_URI'] else app.config['SQLALCHEMY_DATABASE_URI']}")
    
    app.run(host=host, port=port, debug=debug)
