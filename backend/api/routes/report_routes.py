from flask import Blueprint, request, current_app, send_file
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
        "session_id": "DIAG-...",
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
        
        report_format = data.get('format', 'json').lower()
        session_id = data.get('session_id') or data['diagnosis_result'].get('session_id')

        if database_service.db_available and not session_id:
            current_app.logger.warning("Report generation blocked: session_id missing")
            return ResponseFormatter.error(
                message="Session ID is required to generate a persistent report",
                error_code='MISSING_SESSION_ID',
                status_code=400
            )

        # Generate summary report payload
        report = report_generation_service.build_summary_report(
            diagnosis_data=data['diagnosis_result'],
            patient_info=data['patient_info'],
            session_id=session_id
        )

        if report_format == 'pdf':
            report['format'] = 'pdf'
        
        # Save to database if available
        report_id = None
        if database_service.db_available:
            try:
                report_id = database_service.save_report(report, session_id)
            except Exception as e:
                current_app.logger.error("Failed to save report: %s", e)

            if not report_id:
                return ResponseFormatter.error(
                    message="Failed to persist report",
                    error_code='REPORT_PERSISTENCE_ERROR',
                    status_code=500
                )

        # Generate PDF if requested
        if report_format == 'pdf':
            try:
                pdf_buffer = pdf_service.generate_pdf(report, output_path=None)

                if not pdf_buffer:
                    current_app.logger.error("PDF generation failed for report %s", report['report_id'])
                    return (
                        "Failed to generate PDF",
                        500,
                        {"Content-Type": "text/plain"}
                    )

                pdf_buffer.seek(0)
                response = send_file(
                    pdf_buffer,
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=f"{report['report_id']}.pdf"
                )
                response.headers['X-Report-Id'] = report['report_id']
                response.headers['Cache-Control'] = 'no-store'
                current_app.logger.info("PDF generated in memory: %s", report['report_id'])
                return response
            except Exception as e:
                current_app.logger.error("PDF generation error: %s", e, exc_info=True)
                return (
                    "Failed to generate PDF",
                    500,
                    {"Content-Type": "text/plain"}
                )

        # Return JSON response
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
        
        # Get report history
        history = database_service.get_report_history(
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


@report_bp.route('/<report_id>', methods=['GET'])
def get_report(report_id: str):
    """
    Get a single report by report_id.
    """
    try:
        report = database_service.get_report_by_id(report_id)
        if not report:
            return ResponseFormatter.error(
                message="Report not found",
                error_code="REPORT_NOT_FOUND",
                status_code=404
            )

        report_data = report.get('report_data') or report

        return ResponseFormatter.success(
            data=report_data,
            message="Report retrieved successfully"
        )
    except Exception as e:
        current_app.logger.error("Report retrieval error: %s", e, exc_info=True)
        return ResponseFormatter.error(
            message="Failed to retrieve report",
            error_code="REPORT_FETCH_ERROR",
            details=str(e) if current_app.debug else None,
            status_code=500
        )


@report_bp.route('/<report_id>/pdf', methods=['GET'])
def download_report_pdf(report_id: str):
    """
    Download a report PDF by report_id.
    """
    try:
        report = database_service.get_report_by_id(report_id)
        if not report:
            return (
                "Report not found",
                404,
                {"Content-Type": "text/plain"}
            )

        report_data = report.get('report_data') or {}
        if not report_data.get('report_id'):
            report_data['report_id'] = report_id

        pdf_buffer = pdf_service.generate_pdf(report_data, output_path=None)
        if not pdf_buffer:
            current_app.logger.error("PDF generation failed for report %s", report_id)
            return (
                "Failed to generate PDF",
                500,
                {"Content-Type": "text/plain"}
            )

        pdf_buffer.seek(0)
        response = send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{report_id}.pdf"
        )
        response.headers['X-Report-Id'] = report_id
        response.headers['Cache-Control'] = 'no-store'
        return response
    except Exception as e:
        current_app.logger.error("Report PDF error: %s", e, exc_info=True)
        return (
            "Failed to generate PDF",
            500,
            {"Content-Type": "text/plain"}
        )
