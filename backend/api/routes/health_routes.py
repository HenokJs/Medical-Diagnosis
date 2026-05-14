from flask import Blueprint, current_app
from backend.services.ml_service import ml_service
from backend.utils.response_formatter import ResponseFormatter
from backend.app import get_uptime

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    System health check endpoint.
    
    GET /api/v1/health
    
    Returns:
        System health status including model loading status and uptime
    """
    try:
        models_loaded = ml_service.is_loaded()
        
        data = {
            "status": "healthy" if models_loaded else "degraded",
            "models_loaded": models_loaded,
            "uptime": get_uptime(),
            "version": current_app.config["VERSION"],
            "environment": current_app.config["FLASK_ENV"],
        }

        return ResponseFormatter.success(
            data=data,
            message="Health check completed",
            status_code=200 if models_loaded else 503,
        )
        
    except Exception as e:
        current_app.logger.error(f"Health check error: {e}")
        return ResponseFormatter.error(
            message="Health check failed",
            error_code="HEALTH_ERROR",
            status_code=503,
        )


@health_bp.route('/ping', methods=['GET'])
def ping():
    """
    Simple ping endpoint.
    
    GET /api/v1/ping
    """
    return ResponseFormatter.success(
        data={"status": "ok"},
        message="pong",
        status_code=200,
    )
