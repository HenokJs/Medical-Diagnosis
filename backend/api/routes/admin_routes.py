from flask import Blueprint, current_app
from backend.services.ml_service import ml_service
from backend.services.rule_engine_service import rule_engine
from backend.utils.response_formatter import ResponseFormatter

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/model/info', methods=['GET'])
def get_model_info():
    """
    Get ML model information.
    
    GET /api/v1/admin/model/info
    """
    try:
        model_info = ml_service.get_model_info()
        
        return ResponseFormatter.success(
            data=model_info,
            message="Model information retrieved"
        )
        
    except Exception as e:
        current_app.logger.error(f"Model info error: {e}")
        return ResponseFormatter.error(
            message="Failed to retrieve model information",
            error_code="MODEL_INFO_ERROR",
            status_code=500
        )


@admin_bp.route('/diseases', methods=['GET'])
def get_diseases():
    """
    Get list of all diseases.
    
    GET /api/v1/admin/diseases
    """
    try:
        diseases = ml_service.get_all_diseases()
        
        return ResponseFormatter.success(
            data={
                'diseases': diseases,
                'count': len(diseases)
            },
            message=f"Retrieved {len(diseases)} diseases"
        )
        
    except Exception as e:
        current_app.logger.error(f"Get diseases error: {e}")
        return ResponseFormatter.error(
            message="Failed to retrieve diseases",
            error_code="DISEASES_ERROR",
            status_code=500
        )


@admin_bp.route('/symptoms', methods=['GET'])
def get_symptoms():
    """
    Get list of all symptoms.
    
    GET /api/v1/admin/symptoms
    """
    try:
        symptoms = ml_service.get_all_symptoms()
        
        return ResponseFormatter.success(
            data={
                'symptoms': symptoms,
                'count': len(symptoms)
            },
            message=f"Retrieved {len(symptoms)} symptoms"
        )
        
    except Exception as e:
        current_app.logger.error(f"Get symptoms error: {e}")
        return ResponseFormatter.error(
            message="Failed to retrieve symptoms",
            error_code="SYMPTOMS_ERROR",
            status_code=500
        )


@admin_bp.route('/rules', methods=['GET'])
def get_rules():
    """
    Get all clinical rules.
    
    GET /api/v1/admin/rules
    """
    try:
        rules = rule_engine.get_all_rules()
        
        return ResponseFormatter.success(
            data={
                'rules': rules,
                'count': len(rules)
            },
            message=f"Retrieved {len(rules)} clinical rules"
        )
        
    except Exception as e:
        current_app.logger.error(f"Get rules error: {e}")
        return ResponseFormatter.error(
            message="Failed to retrieve rules",
            error_code="RULES_ERROR",
            status_code=500
        )


@admin_bp.route('/stats', methods=['GET'])
def get_system_stats():
    """
    Get system statistics.
    
    GET /api/v1/admin/stats
    """
    try:
        model_info = ml_service.get_model_info()
        diseases = ml_service.get_all_diseases()
        symptoms = ml_service.get_all_symptoms()
        rules = rule_engine.get_all_rules()
        
        stats = {
            'model': {
                'type': model_info.get('model_type'),
                'accuracy': model_info.get('accuracy'),
                'top3_accuracy': model_info.get('top3_accuracy')
            },
            'data': {
                'diseases': len(diseases),
                'symptoms': len(symptoms),
                'rules': len(rules)
            },
            'system': {
                'version': current_app.config['VERSION'],
                'environment': current_app.config['FLASK_ENV']
            }
        }
        
        return ResponseFormatter.success(
            data=stats,
            message="System statistics retrieved"
        )
        
    except Exception as e:
        current_app.logger.error(f"Get stats error: {e}")
        return ResponseFormatter.error(
            message="Failed to retrieve system statistics",
            error_code="STATS_ERROR",
            status_code=500
        )
