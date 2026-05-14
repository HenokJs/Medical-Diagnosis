import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database operations."""
    
    def __init__(self):
        self.db_available = False
        try:
            from backend.database import db
            from backend.models.patient import Patient
            from backend.models.diagnosis import (
                DiagnosisSession,
                ExtractedSymptom,
                DiagnosisPrediction,
                RuleEngineAlert,
            )
            from backend.models.report import Report
            
            self.db = db
            self.Patient = Patient
            self.DiagnosisSession = DiagnosisSession
            self.ExtractedSymptom = ExtractedSymptom
            self.DiagnosisPrediction = DiagnosisPrediction
            self.RuleEngineAlert = RuleEngineAlert
            self.Report = Report
            self.db_available = True
            logger.info("Database service initialized")
        except Exception as e:
            logger.warning(f"Database not available: {e}. Running without persistence.")
    
    def save_diagnosis_session(self, diagnosis_data: Dict, patient_info: Dict) -> Optional[str]:
        """
        Save complete diagnosis session to database.
        
        Args:
            diagnosis_data: Complete diagnosis result
            patient_info: Patient information
            
        Returns:
            Session ID if saved, None if database not available
        """
        if not self.db_available:
            logger.debug("Database not available, skipping save")
            return None
        
        try:
            # Generate session ID
            session_id = f"DIAG-{uuid.uuid4().hex[:12].upper()}"
            
            # Get or create patient
            patient = self._get_or_create_patient(patient_info)
            
            # Create diagnosis session
            session = self.DiagnosisSession(
                session_id=session_id,
                patient_id=patient.id,
                submitted_symptoms=diagnosis_data.get('submitted_symptoms', []),
                free_text_input=diagnosis_data.get('free_text_input'),
                symptom_duration_days=patient_info.get('duration_days'),
                additional_notes=patient_info.get('notes'),
                overall_severity=diagnosis_data['patient_analysis']['severity'],
                risk_level=diagnosis_data['patient_analysis']['risk_level'],
                symptoms_processed=diagnosis_data['patient_analysis']['symptoms_processed'],
                symptoms_matched=diagnosis_data['patient_analysis']['symptoms_matched'],
                processing_time_ms=diagnosis_data.get('processing_time_ms', 0)
            )
            
            self.db.session.add(session)
            self.db.session.flush()  # Get session.id
            
            # Save extracted symptoms
            self._save_extracted_symptoms(session.id, diagnosis_data)
            
            # Save predictions
            self._save_predictions(session.id, diagnosis_data['top_predictions'])
            
            # Save rule engine alerts
            self._save_rule_alerts(session.id, diagnosis_data.get('rule_engine_flags', []))
            
            # Commit transaction
            self.db.session.commit()
            
            logger.info(f"Diagnosis session saved: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to save diagnosis session: {e}")
            self.db.session.rollback()
            return None
    
    def _get_or_create_patient(self, patient_info: Dict):
        """Get existing patient or create new one."""
        patient_id = patient_info.get('patient_id') or f"P-{uuid.uuid4().hex[:8].upper()}"
        age = patient_info.get('age')
        gender = patient_info.get('gender')

        safe_age = age if age is not None else None
        safe_gender = gender if gender else 'unknown'

        patient = self.Patient.query.filter_by(patient_id=patient_id).first()

        if not patient:
            patient = self.Patient(
                patient_id=patient_id,
                age=safe_age,
                gender=safe_gender
            )
            self.db.session.add(patient)
            self.db.session.flush()
            logger.debug(f"Created new patient: {patient_id}")
        else:
            # Update patient info
            if age is not None:
                patient.age = age
            if gender:
                patient.gender = gender
            patient.updated_at = datetime.utcnow()
            logger.debug(f"Updated existing patient: {patient_id}")
        
        return patient
    
    def _save_extracted_symptoms(self, session_id: int, diagnosis_data: Dict):
        """Save extracted symptoms."""
        explainability = diagnosis_data.get('explainability', {})
        matched_symptoms = explainability.get('matched_symptoms', [])
        unmatched_symptoms = explainability.get('unmatched_symptoms', [])
        
        # Save matched symptoms
        for symptom in matched_symptoms:
            extracted = self.ExtractedSymptom(
                session_id=session_id,
                symptom_name=symptom,
                source='merged',
                matched_in_model=True
            )
            self.db.session.add(extracted)
        
        # Save unmatched symptoms
        for symptom in unmatched_symptoms:
            extracted = self.ExtractedSymptom(
                session_id=session_id,
                symptom_name=symptom,
                source='merged',
                matched_in_model=False
            )
            self.db.session.add(extracted)
    
    def _save_predictions(self, session_id: int, predictions: List[Dict]):
        """Save diagnosis predictions."""
        for idx, pred in enumerate(predictions[:3], 1):  # Top-3 only
            prediction = self.DiagnosisPrediction(
                session_id=session_id,
                rank=idx,
                disease_name=pred['disease'],
                confidence_score=pred['confidence'],
                severity=pred.get('severity', 'unknown'),
                description=pred.get('description'),
                matched_symptoms=pred.get('matched_symptoms', []),
                important_features=pred.get('important_features'),
                reasoning=pred.get('reasoning'),
                precautions=pred.get('precautions', []),
                recommendations=pred.get('recommendations', [])
            )
            self.db.session.add(prediction)
    
    def _save_rule_alerts(self, session_id: int, rule_flags: List[Dict]):
        """Save rule engine alerts."""
        # Priority mapping: convert string to integer
        priority_map = {
            'low': 1,
            'medium': 2,
            'high': 3,
            'critical': 4
        }
        
        for flag in rule_flags:
            # Get priority and convert to integer
            priority_value = flag.get('priority', 'medium')
            if isinstance(priority_value, str):
                priority_int = priority_map.get(priority_value.lower(), 2)  # Default to medium (2)
            else:
                priority_int = priority_value if isinstance(priority_value, int) else 2
            
            alert = self.RuleEngineAlert(
                session_id=session_id,
                rule_name=flag.get('name', flag.get('rule', 'Unknown')),
                alert_type=flag.get('type', 'info'),
                message=flag.get('message', flag.get('explanation', '')),
                triggered_by_symptoms=flag.get('triggered_by', []),
                priority=priority_int
            )
            self.db.session.add(alert)
    
    def save_report(self, report_data: Dict, session_id: str = None) -> Optional[str]:
        """
        Save generated report to database.
        
        Args:
            report_data: Report data
            session_id: Associated diagnosis session ID
            
        Returns:
            Report ID if saved, None if database not available
        """
        if not self.db_available:
            return None
        
        try:
            report_id = report_data.get('report_id') or f"RPT-{uuid.uuid4().hex[:12].upper()}"
            
            # Find session if session_id provided
            session = None
            if session_id:
                session = self.DiagnosisSession.query.filter_by(session_id=session_id).first()
                if not session:
                    logger.warning(f"Report save skipped: session not found for {session_id}")
                    return None
            else:
                logger.info("Report save skipped: session_id not provided")
                return None
            
            report = self.Report(
                report_id=report_id,
                session_id=session.id,
                report_type=report_data.get('report_type', 'clinical_summary'),
                format=report_data.get('format', 'json'),
                report_data=report_data,
                file_path=report_data.get('file_path'),
                file_size_bytes=report_data.get('file_size_bytes')
            )
            
            self.db.session.add(report)
            self.db.session.commit()
            
            logger.info(f"Report saved: {report_id}")
            return report_id
            
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
            self.db.session.rollback()
            return None
    
    def get_diagnosis_history(
        self, patient_id: str = None, page: int = 1, limit: int = 50
    ) -> Dict:
        if not self.db_available:
            return {"total": 0, "items": []}
        
        try:
            query = self.DiagnosisSession.query
            
            if patient_id:
                patient = self.Patient.query.filter_by(patient_id=patient_id).first()
                if patient:
                    query = query.filter_by(patient_id=patient.id)
            
            total = query.count()
            sessions = (
                query.order_by(self.DiagnosisSession.created_at.desc())
                .offset((page - 1) * limit)
                .limit(limit)
                .all()
            )

            return {
                "total": total,
                "items": [session.to_dict(include_details=True) for session in sessions],
            }
            
        except Exception as e:
            logger.error(f"Failed to get diagnosis history: {e}")
            return {"total": 0, "items": []}
    
    def get_session_by_id(self, session_id: str) -> Optional[Dict]:
        """
        Get diagnosis session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data or None
        """
        if not self.db_available:
            return None
        
        try:
            session = self.DiagnosisSession.query.filter_by(session_id=session_id).first()
            return session.to_dict(include_details=True) if session else None
        except Exception as e:
            logger.error(f"Failed to get session: {e}")
            return None
    
    def get_statistics(self) -> Dict:
        """
        Get database statistics.
        
        Returns:
            Statistics dictionary
        """
        if not self.db_available:
            return {'database_available': False}
        
        try:
            return {
                'database_available': True,
                'total_patients': self.Patient.query.count(),
                'total_sessions': self.DiagnosisSession.query.count(),
                'total_reports': self.Report.query.count(),
                'recent_sessions': self.DiagnosisSession.query.order_by(
                    self.DiagnosisSession.created_at.desc()
                ).limit(5).count()
            }
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {'database_available': False, 'error': str(e)}


# Singleton instance
database_service = DatabaseService()
