"""
Explainability Service
======================
Generate explainable AI outputs for clinical transparency.

Author: Senior Backend Engineer
Date: 2026-05-11
"""

from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class ExplainabilityService:
    """
    Generate explainable outputs for diagnosis predictions.
    
    Provides:
    - Matched symptoms
    - Important features
    - Confidence reasoning
    - Model transparency
    """
    
    def generate_explanation(self, predictions: List[Dict],
                           matched_symptoms: List[str],
                           important_features: List[Dict],
                           all_symptoms: List[str]) -> Dict:
        """
        Generate comprehensive explanation.
        
        Args:
            predictions: ML predictions
            matched_symptoms: Symptoms that matched features
            important_features: Important features from model
            all_symptoms: All input symptoms
            
        Returns:
            Explainability dictionary
        """
        explanation = {
            'matched_symptoms': matched_symptoms,
            'unmatched_symptoms': [s for s in all_symptoms if s not in matched_symptoms],
            'important_features': important_features,
            'confidence_reasoning': self._generate_confidence_reasoning(predictions),
            'prediction_factors': self._generate_prediction_factors(predictions, matched_symptoms)
        }
        
        return explanation
    
    def _generate_confidence_reasoning(self, predictions: List[Dict]) -> str:
        """Generate confidence reasoning text."""
        if not predictions:
            return "No predictions available"
        
        top_pred = predictions[0]
        confidence = top_pred['confidence']
        
        if confidence > 0.8:
            return f"High confidence ({confidence*100:.1f}%) in primary diagnosis based on strong symptom match"
        elif confidence > 0.5:
            return f"Moderate confidence ({confidence*100:.1f}%) in primary diagnosis. Consider differential diagnoses"
        else:
            return f"Lower confidence ({confidence*100:.1f}%). Multiple conditions possible. Further evaluation recommended"
    
    def _generate_prediction_factors(self, predictions: List[Dict],
                                    matched_symptoms: List[str]) -> List[str]:
        """Generate list of prediction factors."""
        factors = []
        
        if predictions:
            top_disease = predictions[0]['disease']
            factors.append(f"Primary diagnosis: {top_disease}")
        
        if matched_symptoms:
            factors.append(f"Matched {len(matched_symptoms)} clinical symptoms")
        
        if len(predictions) > 1:
            factors.append(f"Differential diagnosis includes {len(predictions)-1} alternative conditions")
        
        return factors


# Global singleton instance
explainability_service = ExplainabilityService()
