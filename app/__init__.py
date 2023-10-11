import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

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

    # Import routes and other components
    from app import routes

    return app
