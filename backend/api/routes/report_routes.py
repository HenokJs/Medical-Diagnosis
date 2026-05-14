from flask import Blueprint, request, current_app, send_file
import os
from backend.services.report_generation_service import report_generation_service
from backend.services.database_service import database_service
from backend.services.pdf_service import pdf_service
from backend.api.middleware.validation import validate_report_request
from backend.utils.response_formatter import ResponseFormatter

report_bp = Blueprint('report', __name__)


@report_bp.route('/generate', methods=['POST'])
def generate_report():
    """
    Generate professional clinical diagnosis report.
    
    POST /api/v1/report/generate
    
    Request Body:
    {
        "diagnosis_result": {...},
        "patient_info": {
            "age": 30,
            "gender": "male",
            "patient_id": "P001"
        },
        "format": "json"  # or "pdf"
    }
    """
    try:
        data = request.get_json(silent=True) or {}
        
        # Validate
        is_valid, error_message = validate_report_request(data)
        if not is_valid:
            return ResponseFormatter.error(
                message=error_message,
                error_code='INVALID_REQUEST',
                status_code=400
            )
        
        # Generate professional clinical report
        report = report_generation_service.generate_clinical_report(
            diagnosis_data=data['diagnosis_result'],
            patient_info=data['patient_info']
        )
        
        # Get format
        report_format = data.get('format', 'json').lower()
        
        # Generate PDF if requested
        if report_format == 'pdf':
            try:
                # Prepare data for PDF
                pdf_data = {
                    'report_id': report['report_id'],
                    'generated_at': report['generated_at'],
                    'patient_info': data['patient_info'],
                    'diagnosis': {
                        'severity': data['diagnosis_result']['patient_analysis'].get('severity', 'unknown'),
                        'risk_level': data['diagnosis_result']['patient_analysis'].get('risk_level', 'unknown'),
                        'top_predictions': data['diagnosis_result']['top_predictions']
                    },
                    'clinical_findings': {
                        'symptoms': data['diagnosis_result'].get('explainability', {}).get('matched_symptoms', []),
                        'rule_flags': data['diagnosis_result'].get('rule_engine_flags', [])
                    },
                    'recommendation': data['diagnosis_result'].get('recommendation', ''),
                    'disclaimer': data['diagnosis_result'].get('disclaimer', '')
                }
                
                # Generate PDF in memory (no file storage)
                pdf_buffer = pdf_service.generate_pdf(pdf_data, output_path=None)
                
                if pdf_buffer:
                    # Update report metadata
                    report['format'] = 'pdf'
                    
                    current_app.logger.info(f"PDF generated in memory: {report['report_id']}")
                    
                    # Return PDF directly from memory
                    from io import BytesIO
                    return send_file(
                        BytesIO(pdf_buffer),
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name=f"{report['report_id']}.pdf"
                    )
                else:
                    current_app.logger.warning("PDF generation failed, falling back to JSON")
                    report_format = 'json'
                    
            except Exception as e:
                current_app.logger.error(f"PDF generation error: {e}")
                report_format = 'json'
        
        # Save to database if available
        try:
            session_id = data['diagnosis_result'].get('session_id')
            database_service.save_report(report, session_id)
        except Exception as e:
            current_app.logger.warning(f"Failed to save report to database: {e}")
        
        # Return JSON response (PDF already returned above if requested)
        return ResponseFormatter.success(
            data=report,
            message="Professional clinical report generated successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Report generation error: {e}", exc_info=True)
        return ResponseFormatter.error(
            message="Failed to generate report",
            error_code="REPORT_ERROR",
            details=str(e) if current_app.debug else None,
            status_code=500
        )


@report_bp.route('/history', methods=['GET'])
def get_report_history():
    """
    Get report history.
    
    GET /api/v1/report/history?patient_id=P001&limit=50
    """
    try:
        patient_id = request.args.get('patient_id')
        page = max(1, int(request.args.get('page', 1)))
        limit = max(1, min(100, int(request.args.get('limit', 50))))
        
        # Get diagnosis history (includes reports)
        history = database_service.get_diagnosis_history(
            patient_id=patient_id,
            page=page,
            limit=limit,
        )

        return ResponseFormatter.success(
            data={
                'history': history['items'],
                'total': history['total'],
                'page': page,
                'limit': limit,
            },
            message="Report history retrieved successfully",
        )
        
    except Exception as e:
        current_app.logger.error(f"Report history error: {e}", exc_info=True)
        return ResponseFormatter.error(
            message="Failed to retrieve report history",
            error_code="HISTORY_ERROR",
            details=str(e) if current_app.debug else None,
            status_code=500
        )
