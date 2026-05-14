import os
import logging
from urllib.parse import urlparse
from flask import Flask
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv

from backend.config import get_config
from backend.database import init_db


load_dotenv()

# Application start time for uptime calculation
APP_START_TIME = datetime.utcnow()


def create_app(config_name=None):
    app = Flask(__name__)
    
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    setup_logging(app)
    
    initialize_database(app)
    
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    create_directories(app)
    
    initialize_ml_models(app)
    
    register_blueprints(app)
    
    register_error_handlers(app)
    
    register_middleware(app)
    
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    db_host = "unknown"
    if db_uri:
        parsed = urlparse(db_uri)
        db_host = parsed.hostname or parsed.path

    app.logger.info("Application started: %s v%s", app.config["APP_NAME"], app.config["VERSION"])
    app.logger.info("Environment: %s", app.config["FLASK_ENV"])
    app.logger.info("Database host: %s", db_host)
    
    return app


def setup_logging(app):
    log_dir = app.config['LOG_DIR']
    os.makedirs(log_dir, exist_ok=True)
    
    log_level = getattr(logging, app.config['LOG_LEVEL'])
    
    log_file = os.path.join(log_dir, 'app.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    
    app.logger.handlers = []
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    logging.getLogger('werkzeug').setLevel(logging.WARNING)


def initialize_database(app):
    try:
        app.logger.info("Initializing database...")
        init_db(app)
        app.logger.info("Database initialized successfully")
        
    except Exception as e:
        app.logger.error(f"Failed to initialize database: {e}")
        app.logger.warning("Application will continue without database persistence")


def create_directories(app):
    directories = [
        app.config['LOG_DIR'],
        app.config['REPORT_DIR'],
        app.config['REPORT_TEMPLATE_DIR']
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        app.logger.debug(f"Directory ensured: {directory}")


def initialize_ml_models(app):
    try:
        if app.config.get("SKIP_MODEL_LOAD"):
            app.logger.info("Skipping ML model loading")
            return

        from backend.services.ml_service import ml_service
        
        model_dir = app.config['MODEL_DIR']
        dataset_dir = app.config['DATASET_DIR']
        
        app.logger.info("Loading ML models...")
        ml_service.load_models(model_dir, dataset_dir)
        app.logger.info("ML models loaded successfully")
        
    except Exception as e:
        app.logger.error(f"Failed to load ML models: {e}")
        raise


def register_blueprints(app):
    from backend.api.routes.diagnosis_routes import diagnosis_bp
    from backend.api.routes.health_routes import health_bp
    from backend.api.routes.admin_routes import admin_bp
    from backend.api.routes.report_routes import report_bp
    
    # Register with API prefix
    api_prefix = app.config['API_PREFIX']
    
    app.register_blueprint(diagnosis_bp, url_prefix=f"{api_prefix}/diagnosis")
    app.register_blueprint(health_bp, url_prefix=f"{api_prefix}")
    app.register_blueprint(admin_bp, url_prefix=f"{api_prefix}/admin")
    app.register_blueprint(report_bp, url_prefix=f"{api_prefix}/report")
    
    app.logger.info("Blueprints registered")


def register_error_handlers(app):
    from backend.api.middleware.error_handler import (
        handle_400, handle_404, handle_500, handle_generic_exception
    )
    
    app.register_error_handler(400, handle_400)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)
    app.register_error_handler(Exception, handle_generic_exception)
    
    app.logger.info("Error handlers registered")


def register_middleware(app):
    if app.config.get("LOG_REQUESTS"):
        from backend.api.middleware.request_logger import log_request, log_response

        app.before_request(log_request)
        app.after_request(log_response)

        app.logger.info("Request logging enabled")


def get_uptime():
    uptime_delta = datetime.utcnow() - APP_START_TIME
    
    days = uptime_delta.days
    hours, remainder = divmod(uptime_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"
