"""
Diagnosis Controller
====================
Orchestrates diagnosis workflow across all services.

Author: Senior Backend Engineer
Date: 2026-05-11
"""

from typing import Dict, List
import logging
from flask import current_app

from api.services.ml_service import ml_service
from api.services.rule_engine_service import rule_engine
from api.services.nlp_service import nlp_service
from api.services.severity_service import severity_service
from api.services.explainability_service import explainability_service

logger = logging.getLogger(__name__)


class DiagnosisController:
    """
    Main diagnosis controller.
    
    Orchestrates:
    - NLP symptom processing
    - ML prediction
    - Rule engine evaluation
    - Severity assessment
    - Explainability generation
    """
    
    def predict_diagnosis(self, data: Dict) -> Dict:
        """
        Complete diagnosis prediction workflow.
        
        Args:
            data: Request data containing symptoms and patient info
            
        Returns:
            Complete diagnosis response
        """
        logger.info("Starting diagnosis prediction")
        
        # Extract input data
        structured_symptoms = data.get('symptoms', [])
        free_text = data.get('free_text', '')
        age = data.get('age')
        gender = data.get('gender')
        duration_days = data.get('duration_days')
        
        # Step 1: Process symptoms with NLP
        all_symptoms = nlp_service.process_input(
            structured_symptoms=structured_symptoms,
            free_text=free_text
        )
        logger.info(f"Processed symptoms: {all_symptoms}")
        
        if not all_symptoms:
            raise ValueError("No valid symptoms provided")
        
        # Step 2: Get ML predictions
        predictions = ml_service.predict(
            symptoms=all_symptoms,
            top_k=current_app.config['TOP_K_PREDICTIONS']
        )
        logger.info(f"ML predictions: {[p['disease'] for p in predictions]}")
        
        # Step 3: Evaluate rule engine
        rule_flags = rule_engine.evaluate_symptoms(
            symptoms=all_symptoms,
            duration_days=duration_days,
            age=age
        )
        logger.info(f"Rule engine flags: {len(rule_flags)}")
        
        # Step 4: Assess severity and risk
        risk_level = rule_engine.get_risk_level(rule_flags)
        overall_severity = severity_service.assess_overall_severity(
            predictions=predictions,
            rule_flags=rule_flags
        )
        
        # Step 5: Generate explainability
        matched_symptoms = ml_service.get_matched_symptoms(all_symptoms)
        important_features = ml_service.get_feature_importance(all_symptoms)
        
        explainability = explainability_service.generate_explanation(
            predictions=predictions,
            matched_symptoms=matched_symptoms,
            important_features=important_features,
            all_symptoms=all_symptoms
        )
        
        # Step 6: Generate recommendation
        recommendation = rule_engine.generate_recommendation(
            triggered_rules=rule_flags,
            risk_level=risk_level
        )
        
        # Step 7: Build response
        response = {
            'success': True,
            'patient_analysis': {
                'severity': overall_severity,
                'risk_level': risk_level,
                'symptoms_processed': len(all_symptoms),
                'symptoms_matched': len(matched_symptoms),
                'age': age,
                'gender': gender,
                'duration_days': duration_days
            },
            'top_predictions': predictions,
            'explainability': explainability,
            'rule_engine_flags': rule_flags,
            'recommendation': recommendation,
            'disclaimer': current_app.config['MEDICAL_DISCLAIMER']
        }
        
        logger.info("Diagnosis prediction completed successfully")
        return response
    
    def analyze_symptoms(self, data: Dict) -> Dict:
        """
        Detailed symptom analysis.
        
        Args:
            data: Request data
            
        Returns:
            Detailed analysis response
        """
        logger.info("Starting symptom analysis")
        
        # Process symptoms
        structured_symptoms = data.get('symptoms', [])
        free_text = data.get('free_text', '')
        
        all_symptoms = nlp_service.process_input(
            structured_symptoms=structured_symptoms,
            free_text=free_text
        )
        
        if not all_symptoms:
            raise ValueError("No valid symptoms provided")
        
        # Get matched symptoms
        matched_symptoms = ml_service.get_matched_symptoms(all_symptoms)
        unmatched_symptoms = [s for s in all_symptoms if s not in matched_symptoms]
        
        # Get feature importance
        important_features = ml_service.get_feature_importance(all_symptoms, top_n=10)
        
        # Evaluate rules
        rule_flags = rule_engine.evaluate_symptoms(
            symptoms=all_symptoms,
            duration_days=data.get('duration_days'),
            age=data.get('age')
        )
        
        # Build analysis response
        response = {
            'input_symptoms': {
                'structured': structured_symptoms,
                'free_text': free_text,
                'processed': all_symptoms
            },
            'symptom_matching': {
                'matched': matched_symptoms,
                'unmatched': unmatched_symptoms,
                'match_rate': len(matched_symptoms) / len(all_symptoms) if all_symptoms else 0
            },
            'feature_importance': important_features,
            'rule_evaluation': {
                'triggered_rules': rule_flags,
                'risk_level': rule_engine.get_risk_level(rule_flags)
            }
        }
        
        logger.info("Symptom analysis completed")
        return response
    
    def batch_diagnosis(self, patients: List[Dict]) -> List[Dict]:
        """
        Process batch diagnosis for multiple patients.
        
        Args:
            patients: List of patient data
            
        Returns:
            List of diagnosis results
        """
        logger.info(f"Starting batch diagnosis for {len(patients)} patients")
        
        results = []
        
        for idx, patient_data in enumerate(patients):
            try:
                # Add patient ID if not present
                if 'patient_id' not in patient_data:
                    patient_data['patient_id'] = f"P{idx+1:03d}"
                
                # Get diagnosis
                diagnosis = self.predict_diagnosis(patient_data)
                
                # Add patient ID to result
                diagnosis['patient_id'] = patient_data['patient_id']
                
                results.append(diagnosis)
                
            except Exception as e:
                logger.error(f"Error processing patient {patient_data.get('patient_id', idx)}: {e}")
                results.append({
                    'patient_id': patient_data.get('patient_id', f"P{idx+1:03d}"),
                    'success': False,
                    'error': str(e)
                })
        
        logger.info(f"Batch diagnosis completed: {len(results)} results")
        return results
