import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()  # Create a LoginManager instance
login_manager.login_view = 'auth.login'  # Set the login view

def create_app(config_filename='config.py'):
    app = Flask(__name__)

    # Get the current directory of this script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to config.py in the root directory
    config_path = os.path.join(current_directory, '..', config_filename)

    # Load the configuration
    app.config.from_pyfile(config_path)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Initialize the LoginManager with the app
    login_manager.init_app(app)  # Initialize LoginManager

    # Import routes and other components
    from app import routes
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.landing import landing_bp
    from app.routes.settings import settings_bp
    from app.routes.transactions import transactions_bp
    from app.routes.reports import reports_bp
    

    # Register the blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(landing_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(reports_bp)

    return app
