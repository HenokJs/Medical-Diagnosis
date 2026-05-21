import logging
from datetime import datetime
from typing import Dict
import uuid

logger = logging.getLogger(__name__)


class ReportGenerationService:
    """Service for generating professional clinical reports."""

    def build_summary_report(
        self,
        diagnosis_data: Dict,
        patient_info: Dict,
        session_id: str | None = None,
    ) -> Dict:
        """
        Build a summary report payload for API responses and PDF generation.
        """

        report_id = f"RPT-{uuid.uuid4().hex[:12].upper()}"
        timestamp = datetime.utcnow().isoformat()

        patient_payload = {
            'age': patient_info.get('age'),
            'gender': patient_info.get('gender'),
            'patient_id': patient_info.get('patient_id'),
            'name': patient_info.get('name')
        }

        patient_analysis = diagnosis_data.get('patient_analysis', {})
        explainability = diagnosis_data.get('explainability', {})

        report = {
            'report_id': report_id,
            'session_id': session_id,
            'report_type': 'clinical_summary',
            'generated_at': timestamp,
            'format': 'json',
            'patient_info': patient_payload,
            'diagnosis': {
                'severity': patient_analysis.get('severity', 'unknown'),
                'risk_level': patient_analysis.get('risk_level', 'unknown'),
                'top_predictions': self._normalize_predictions(
                    diagnosis_data.get('top_predictions', [])
                ),
            },
            'clinical_findings': {
                'symptoms': explainability.get('matched_symptoms', []),
                'rule_flags': diagnosis_data.get('rule_engine_flags', []),
            },
            'recommendation': diagnosis_data.get('recommendation', ''),
            'disclaimer': diagnosis_data.get('disclaimer', ''),
        }

        logger.info("Summary report generated: %s", report_id)
        return report

    def generate_clinical_report(self, diagnosis_data: Dict, patient_info: Dict) -> Dict:
        """
        Generate a comprehensive clinical report.
        """

        report_id = f"RPT-{uuid.uuid4().hex[:12].upper()}"
        timestamp = datetime.utcnow()

        report = {
            'report_id': report_id,
            'report_type': 'clinical_summary',
            'generated_at': timestamp.isoformat(),
            'format': 'json',

            # Patient Information
            'patient_information': self._build_patient_section(patient_info),

            # Submitted Symptoms
            'submitted_symptoms': self._build_symptoms_section(diagnosis_data),

            # AI Diagnostic Analysis
            'diagnostic_analysis': self._build_analysis_section(diagnosis_data),

            # Clinical Reasoning
            'clinical_reasoning': self._build_reasoning_section(diagnosis_data),

            # Severity Assessment
            'severity_assessment': self._build_severity_section(diagnosis_data),

            # Risk Modifiers
            'risk_modifiers': self._build_risk_modifiers_section(
                diagnosis_data,
                patient_info
            ),

            # Treatment Guidance
            'treatment_guidance': self._build_treatment_section(diagnosis_data),

            # Clinical Alerts
            'clinical_alerts': diagnosis_data.get('rule_engine_flags', []),

            # Medical Disclaimer
            'medical_disclaimer': diagnosis_data.get('disclaimer', ''),

            # Metadata
            'metadata': {
                'processing_time_ms': diagnosis_data.get('processing_time_ms', 0),
                'model_version': '1.0.0',
                'report_version': '1.0.0'
            }
        }

        logger.info(f"Clinical report generated: {report_id}")

        return report

    def _normalize_predictions(self, predictions: list[Dict]) -> list[Dict]:
        """Normalize prediction payloads for report rendering."""
        normalized: list[Dict] = []

        for pred in predictions:
            confidence = pred.get('confidence')
            if confidence is None:
                confidence = pred.get('confidence_score')

            normalized.append({
                'disease': pred.get('disease') or pred.get('disease_name') or 'Unknown',
                'confidence': confidence or 0,
                'severity': pred.get('severity', 'unknown'),
                'description': pred.get('description'),
                'precautions': pred.get('precautions', []),
                'recommendations': pred.get('recommendations', []),
            })

        return normalized

    def _build_patient_section(self, patient_info: Dict) -> Dict:
        """Build patient information section."""

        symptom_duration = (
            patient_info.get('symptom_duration')
            or patient_info.get('symptomDuration')
        )

        return {
            'age': patient_info.get('age'),
            'gender': patient_info.get('gender'),
            'symptom_duration': symptom_duration or 'Not specified',
            'duration_days': patient_info.get('duration_days'),
            'additional_notes': patient_info.get('notes', 'None'),
            'report_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        }

    def _build_symptoms_section(self, diagnosis_data: Dict) -> Dict:
        """Build submitted symptoms section."""

        patient_analysis = diagnosis_data.get('patient_analysis', {})

        return {
            'checkbox_symptoms': diagnosis_data.get('submitted_symptoms', []),
            'free_text_input': diagnosis_data.get('free_text_input', ''),
            'total_symptoms_processed': patient_analysis.get(
                'symptoms_processed',
                0
            ),
            'symptoms_matched_in_model': patient_analysis.get(
                'symptoms_matched',
                0
            )
        }

    def _build_analysis_section(self, diagnosis_data: Dict) -> Dict:
        """Build AI diagnostic analysis section."""

        predictions = diagnosis_data.get('top_predictions', [])[:3]

        top_3 = []

        for idx, pred in enumerate(predictions):
            disease_name = (
                pred.get('disease')
                or pred.get('disease_name')
                or 'Unknown'
            )

            confidence = (
                pred.get('confidence')
                or pred.get('confidence_score')
                or 0
            )

            top_3.append({
                'rank': idx + 1,
                'disease': disease_name,
                'confidence_percentage': round(confidence * 100, 1),
                'severity': pred.get('severity', 'Unknown'),
                'description': pred.get('description', ''),
                'matched_symptoms': pred.get('matched_symptoms', [])
            })

        primary_prediction = predictions[0] if predictions else {}

        primary_disease = (
            primary_prediction.get('disease')
            or primary_prediction.get('disease_name')
            or 'Unknown'
        )

        primary_confidence = (
            primary_prediction.get('confidence')
            or primary_prediction.get('confidence_score')
            or 0
        )

        return {
            'top_3_diagnoses': top_3,

            'primary_diagnosis': {
                'disease': primary_disease,
                'confidence': round(primary_confidence * 100, 1),
                'severity': primary_prediction.get('severity', 'Unknown')
            }
        }

    def _build_reasoning_section(self, diagnosis_data: Dict) -> Dict:
        """Build clinical reasoning section."""

        explainability = diagnosis_data.get('explainability', {})

        return {
            'matched_symptoms': explainability.get(
                'matched_symptoms',
                []
            ),

            'unmatched_symptoms': explainability.get(
                'unmatched_symptoms',
                []
            ),

            'influential_symptoms': explainability.get(
                'important_features',
                []
            )[:5],

            'confidence_factors': explainability.get(
                'confidence_reasoning',
                'Based on symptom pattern analysis'
            ),

            'reasoning_summary': self._generate_reasoning_summary(
                diagnosis_data
            )
        }

    def _generate_reasoning_summary(self, diagnosis_data: Dict) -> str:
        """Generate a reasoning summary."""

        predictions = diagnosis_data.get('top_predictions', [])

        if not predictions:
            return "No diagnostic predictions were generated."

        top_prediction = predictions[0]

        top_disease = (
            top_prediction.get('disease')
            or top_prediction.get('disease_name')
            or 'Unknown Condition'
        )

        confidence = (
            top_prediction.get('confidence')
            or top_prediction.get('confidence_score')
            or 0
        )

        patient_analysis = diagnosis_data.get('patient_analysis', {})

        matched = patient_analysis.get('symptoms_matched', 0)

        return (
            f"The AI system identified {top_disease} as the most likely "
            f"condition with {confidence * 100:.1f}% confidence. "
            f"This assessment is based on {matched} matched symptoms "
            f"and clinical pattern recognition."
        )

    def _build_severity_section(self, diagnosis_data: Dict) -> Dict:
        """Build severity assessment section."""

        patient_analysis = diagnosis_data.get('patient_analysis', {})

        severity_descriptions = {
            'minor': (
                'Minor condition - typically self-limiting '
                'and manageable at home'
            ),

            'moderate': (
                'Moderate condition - may require medical consultation'
            ),

            'urgent': (
                'Urgent condition - medical attention recommended soon'
            ),

            'critical': (
                'Critical condition - immediate medical attention required'
            )
        }

        severity = patient_analysis.get('severity', 'unknown')

        return {
            'overall_severity': severity,

            'severity_description': severity_descriptions.get(
                severity,
                'Severity assessment unavailable'
            ),

            'risk_level': patient_analysis.get(
                'risk_level',
                'unknown'
            ),

            'urgency_recommendation': self._get_urgency_recommendation(
                severity
            )
        }

    def _get_urgency_recommendation(self, severity: str) -> str:
        """Get urgency recommendation based on severity."""

        recommendations = {
            'minor': (
                'Monitor symptoms. Consult healthcare provider '
                'if symptoms worsen or persist.'
            ),

            'moderate': (
                'Schedule an appointment with your healthcare '
                'provider within 1-2 days.'
            ),

            'urgent': (
                'Seek medical attention within 24 hours '
                'or visit urgent care.'
            ),

            'critical': (
                'Seek immediate emergency medical attention. '
                'Call emergency services if needed.'
            )
        }

        return recommendations.get(
            severity,
            'Consult with a healthcare professional for guidance.'
        )

    def _build_risk_modifiers_section(
        self,
        diagnosis_data: Dict,
        patient_info: Dict
    ) -> Dict:
        """Build risk modifiers section."""

        age = patient_info.get('age', 0)
        gender = patient_info.get('gender', 'unknown')

        modifiers = []

        # Age-based modifiers
        if age < 5:
            modifiers.append({
                'type': 'age',
                'factor': 'Pediatric patient',
                'impact': (
                    'Increased monitoring recommended '
                    'for young children'
                )
            })

        elif age > 65:
            modifiers.append({
                'type': 'age',
                'factor': 'Elderly patient',
                'impact': (
                    'Higher risk for complications; '
                    'closer monitoring advised'
                )
            })

        # Gender-based modifiers
        if gender == 'female':
            modifiers.append({
                'type': 'gender',
                'factor': 'Female patient',
                'impact': (
                    'Consider pregnancy status and '
                    'gender-specific conditions'
                )
            })

        return {
            'modifiers_applied': len(modifiers) > 0,
            'risk_factors': modifiers,
            'summary': (
                f"{len(modifiers)} risk modifier(s) "
                f"considered in assessment"
            )
        }

    def _build_treatment_section(self, diagnosis_data: Dict) -> Dict:
        """Build treatment guidance section."""

        patient_analysis = diagnosis_data.get('patient_analysis', {})
        severity = patient_analysis.get('severity', 'unknown')

        general_recommendations = [
            'Stay well hydrated with water and clear fluids',
            'Get adequate rest and sleep',
            'Monitor symptoms and track any changes',
            'Maintain good nutrition',
            'Avoid strenuous activities if feeling unwell'
        ]

        severity_specific = {
            'minor': [
                'Self-care measures may be sufficient',
                'Over-the-counter remedies may provide relief',
                'Contact healthcare provider if symptoms worsen'
            ],

            'moderate': [
                'Schedule appointment with healthcare provider',
                'Keep a symptom diary',
                'Follow up if no improvement in 2-3 days'
            ],

            'urgent': [
                'Seek medical attention promptly',
                'Do not delay professional evaluation',
                'Have someone accompany you if possible'
            ],

            'critical': [
                'Seek immediate emergency care',
                'Call emergency services if needed',
                'Do not attempt to drive yourself'
            ]
        }

        return {
            'general_recommendations': general_recommendations,

            'severity_specific_guidance': severity_specific.get(
                severity,
                []
            ),

            'important_notes': [
                'These are general wellness recommendations only',
                'NOT a substitute for professional medical advice',
                'Do NOT self-prescribe medications',
                'Always consult healthcare provider for treatment decisions'
            ],

            'when_to_seek_help': [
                'Symptoms worsen or do not improve',
                'New symptoms develop',
                'Difficulty breathing or chest pain',
                'High fever that does not respond to treatment',
                'Severe pain or discomfort'
            ]
        }

    def generate_printable_html(self, report_data: Dict) -> str:
        """
        Generate HTML version of report for printing.
        """

        return f"""
        <html>
        <head>
            <title>Clinical Report</title>
        </head>

        <body>
            <h1>Clinical Report</h1>
            <h2>Report ID: {report_data['report_id']}</h2>

            <p>
                Generated at:
                {report_data['generated_at']}
            </p>
        </body>
        </html>
        """


# Singleton instance
report_generation_service = ReportGenerationService()