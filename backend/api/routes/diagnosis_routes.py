from flask import Blueprint, request, current_app
from backend.api.controllers.diagnosis_controller import DiagnosisController
from backend.api.middleware.validation import validate_diagnosis_request
from backend.utils.response_formatter import ResponseFormatter

diagnosis_bp = Blueprint('diagnosis', __name__)
controller = DiagnosisController()


@diagnosis_bp.route('/predict', methods=['POST'])
def predict_diagnosis():
    """
    Main diagnosis prediction endpoint.
    
    POST /api/v1/diagnosis/predict
    
    Request Body:
    {
        "symptoms": ["fever", "cough", "fatigue"],
        "age": 29,
        "gender": "male",
        "duration_days": 4,
        "free_text": "I have fever and body pain"
    }
    
    Returns:
        Diagnosis prediction with top-3 diseases, confidence scores,
        severity, explainability, and clinical recommendations.
    """
    try:
        data = request.get_json(silent=True) or {}
        
        # Validate request
        is_valid, error_message = validate_diagnosis_request(data)
        if not is_valid:
            return ResponseFormatter.error(
                message=error_message,
                error_code='INVALID_REQUEST',
                status_code=400
            )
        
        result = controller.predict_diagnosis(data)
        
        return ResponseFormatter.success(
            data=result,
            message="Diagnosis completed successfully"
        )
        
    except ValueError as e:
        current_app.logger.error(f"Validation error: {e}")
        return ResponseFormatter.error(
            message=str(e),
            error_code='VALIDATION_ERROR',
            status_code=400
        )
    
    except Exception as e:
        current_app.logger.error(f"Diagnosis error: {e}", exc_info=True)
        return ResponseFormatter.error(
            message="An error occurred during diagnosis",
            error_code='DIAGNOSIS_ERROR',
            details=str(e) if current_app.debug else None,
            status_code=500
        )


@diagnosis_bp.route('/analyze', methods=['POST'])
def analyze_symptoms():
    """
    Detailed symptom analysis endpoint.
    
    POST /api/v1/diagnosis/analyze
    
    Provides detailed analysis including:
    - Symptom matching
    - Feature importance
    - Rule engine evaluation
    - Risk assessment
    """
    try:
        data = request.get_json(silent=True) or {}
        
        # Validate
        is_valid, error_message = validate_diagnosis_request(data)
        if not is_valid:
            return ResponseFormatter.error(
                message=error_message,
                error_code='INVALID_REQUEST',
                status_code=400
            )
        
        # Analyze
        result = controller.analyze_symptoms(data)
        
        return ResponseFormatter.success(
            data=result,
            message="Analysis completed successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Analysis error: {e}", exc_info=True)
        return ResponseFormatter.error(
            message="An error occurred during analysis",
            error_code='ANALYSIS_ERROR',
            details=str(e) if current_app.debug else None,
            status_code=500
        )


@diagnosis_bp.route('/batch', methods=['POST'])
def batch_diagnosis():
    """
    Batch diagnosis endpoint for multiple patients.
    
    POST /api/v1/diagnosis/batch
    
    Request Body:
    {
        "patients": [
            {
                "patient_id": "P001",
                "symptoms": ["fever", "cough"],
                "age": 30,
                "gender": "male"
            },
            ...
        ]
    }
    """
    try:
        data = request.get_json(silent=True) or {}
        
        if 'patients' not in data or not isinstance(data['patients'], list):
            return ResponseFormatter.error(
                message="Invalid batch request format",
                error_code='INVALID_BATCH_REQUEST',
                status_code=400
            )
        
        # Process batch
        results = controller.batch_diagnosis(data['patients'])
        
        return ResponseFormatter.success(
            data={'results': results, 'count': len(results)},
            message=f"Batch diagnosis completed for {len(results)} patients"
        )
        
    except Exception as e:
        current_app.logger.error(f"Batch diagnosis error: {e}", exc_info=True)
        return ResponseFormatter.error(
            message="An error occurred during batch diagnosis",
            error_code='BATCH_ERROR',
            details=str(e) if current_app.debug else None,
            status_code=500
        )
