"""
Severity Service
================
Clinical severity assessment service.

Author: Senior Backend Engineer
Date: 2026-05-11
"""

from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class SeverityService:
    """
    Assess clinical severity based on multiple factors.
    
    Severity Levels:
    - minor: Low-risk conditions
    - moderate: Moderate-risk conditions
    - urgent: High-risk conditions requiring prompt attention
    - critical: Life-threatening conditions requiring immediate attention
    """
    
    def assess_overall_severity(self, predictions: List[Dict],
                               rule_flags: List[Dict]) -> str:
        """
        Assess overall severity from predictions and rules.
        
        Args:
            predictions: ML predictions with severity
            rule_flags: Triggered rule flags
            
        Returns:
            Overall severity level
        """
        # Get severity from top prediction
        top_prediction_severity = predictions[0]['severity'] if predictions else 'unknown'
        
        # Get severity from rules
        rule_priorities = [rule['priority'] for rule in rule_flags]
        
        # Determine overall severity
        if 'critical' in rule_priorities:
            return 'critical'
        elif 'high' in rule_priorities or top_prediction_severity == 'urgent':
            return 'urgent'
        elif 'medium' in rule_priorities or top_prediction_severity == 'moderate':
            return 'moderate'
        else:
            return 'minor'
    
    def get_severity_description(self, severity: str) -> str:
        """Get human-readable severity description."""
        descriptions = {
            'minor': 'Low-risk condition. Monitor symptoms and seek care if they worsen.',
            'moderate': 'Moderate-risk condition. Schedule medical consultation within 24-48 hours.',
            'urgent': 'High-risk condition. Seek medical attention promptly today.',
            'critical': 'Critical condition. Seek immediate emergency medical attention.'
        }
        return descriptions.get(severity, 'Unknown severity level')


# Global singleton instance
severity_service = SeverityService()
